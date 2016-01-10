import logging
import os
import sys
from multiprocessing import Queue

import phue
import yaml
from PyQt4 import QtGui, QtCore
from updater4pyi import upd_source, upd_core, upd_log
from updater4pyi.upd_iface_pyqt4 import UpdatePyQt4Interface

# UI
import twitch_bot.gui.forms.main_window as main_window
import twitch_bot.gui.forms.hue_retry_box as hue_retry_box
from twitch_bot.gui import config_window

from config_schema import AppConfig
from twitch_hue_bot import TwitchHueBot
from log import get_logger
from version import package_version

if sys.platform == 'win32':
  pass

logger = get_logger(__name__)

# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
  def __init__(self,queue):
    self.queue = queue

  def write(self, text):
    self.queue.put(text)

  def flush(self):
    pass

# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal
class MyReceiver(QtCore.QObject):
  mysignal = QtCore.pyqtSignal(str)

  def __init__(self,queue,*args,**kwargs):
    QtCore.QObject.__init__(self,*args,**kwargs)
    self.queue = queue
    self.running = True

  def stop_processing(self):
    self.running = False

  @QtCore.pyqtSlot()
  def run(self):
    while self.running:
      text = self.queue.get()
      self.mysignal.emit(text)

class HueRetryBox(QtGui.QDialog, hue_retry_box.Ui_Dialog):
  def __init__(self, parent=None):
    super(HueRetryBox, self).__init__(parent)
    self.setupUi(self)

    self.button_box.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
    self.button_box.button(QtGui.QDialogButtonBox.Retry).clicked.connect(self.retry)

  def retry(self):
    self.close()

class MainWindow(QtGui.QMainWindow, main_window.Ui_main_window):
  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)
    self.setupUi(self)

    self.config_button.clicked.connect(self.open_config)
    self.start_button.clicked.connect(self.start_bot)

    self.config_gui = config_window.ConfigWindow()
    self.config_gui.hide()

    self.bot_thread = None
    self.receiver_thread = None
    self.receiver = None

  def closeEvent(self, event):
    logger.debug("Closing!")
    if self.receiver:
      self.receiver.stop_processing()
    if self.receiver_thread:
      self.receiver_thread.exit()
    event.accept()

  def open_config(self):
    self.config_gui.load()
    self.config_gui.show()

  def update_list(self, line):
    self.text_list.addItem(line)
    self.text_list.scrollToBottom()

  class BotThread(QtCore.QThread):

    def run(self):
      if os.path.isfile("config.yml"):
        raw_config = yaml.load(open("config.yml", 'r')) or {}
        config = AppConfig.to_python(raw_config)

        bot = TwitchHueBot(config)

        logger.info("Config: %s", AppConfig.from_python(config))
        try:
          bot.run()
        except phue.PhueRegistrationException as e:
          logger.error("Failed to register with the Hue Bridge. Push the button on the bridge.")
        except Exception as e:
          logger.error("Failed to start bot.")
          raise e

  def test_hue_connection(self, config):
    def cancel():
      raise Exception("Cancelled retry process.")

    def retry():
      self.test_hue_connection(config)

    try:
      phue.Bridge(config['hue']['bridge-ip'])
    except Exception as e:
      logger.error(e.message)
      dialog = HueRetryBox()
      dialog.button_box.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(cancel)
      dialog.button_box.button(QtGui.QDialogButtonBox.Retry).clicked.connect(retry)

      dialog.exec_()

  def start_bot(self):
    self.start_button.setEnabled(False)

    if os.path.isfile("config.yml"):
      raw_config = yaml.load(open("config.yml", 'r')) or {}
      config = AppConfig.to_python(raw_config)
      self.test_hue_connection(AppConfig.from_python(config))
      self.bot_thread = self.BotThread()
      self.bot_thread.daemon = True
      self.bot_thread.start()

def main():
  app = QtGui.QApplication(sys.argv)
  form = MainWindow()

  queue = Queue()
  sys.stdout = WriteStream(queue)

  # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
  thread = QtCore.QThread()
  my_receiver = MyReceiver(queue)
  my_receiver.mysignal.connect(form.update_list)
  my_receiver.moveToThread(thread)
  thread.started.connect(my_receiver.run)
  thread.start()

  form.receiver_thread = thread
  form.receiver = my_receiver
  form.show()

  # Only tested for Windows currently
  if sys.platform == 'win32':
    update_thread = check_for_update(queue)

  app.exec_()

class UpdateThread(QtCore.QThread):
  def __init__(self, q):
    super(UpdateThread, self).__init__()
    self.queue = q
    sys.stdout = WriteStream(q)

  #Load saved settings, if any.
  def save_config(self, config):
    with open("config.yml", "w") as config_file:
      noalias_dumper = yaml.dumper.SafeDumper
      noalias_dumper.ignore_aliases = lambda self, data: True

      file_contents = yaml.dump(config,
                                default_flow_style=False,
                                Dumper=noalias_dumper)

      config_file.write(file_contents)

  def load_config (self):
    if os.path.isfile("config.yml"):
      raw_config = yaml.load(open("config.yml", 'r')) or {}
      self.logger.info('raw_config')
      return AppConfig.to_python(raw_config)
    return {}

  def run(self):
    try:
      stream = WriteStream(self.queue)
      upd_log.setup_logger(1)

      ch = logging.StreamHandler(stream)
      ch.setLevel(logging.DEBUG)
      upd_log.logger.addHandler(ch)
      logger.addHandler(ch)

      swu_source = upd_source.UpdateGithubReleasesSource('gibsonje/hue-subscriber-bot')
      swu_updater = upd_core.Updater( current_version=package_version,
                                      update_source=swu_source)
      swu_interface = UpdatePyQt4Interface(swu_updater,
                            progname='hue-subscriber-bot',
                            ask_before_checking=False,

                            parent=QtGui.QApplication.instance())

      config = self.load_config()
      if config.get('use_updater', True):
        available_update = swu_updater.check_for_updates()
        logger.info("Current Version: %s", swu_updater.current_version())

        if available_update:
          logger.info("Update available!")
          if swu_interface.ask_to_update(available_update):
            def download_file(url, fdst):
              import requests
              logger.debug("fetching URL %s to temp file...", url)

              r = requests.get(url, stream=True)
              for chunk in r.iter_content(chunk_size=1024):
                  if chunk: # filter out keep-alive new chunks
                      fdst.write(chunk)

              logger.debug("... done.")
            swu_updater.download_file = download_file
            swu_updater.install_update(available_update)
        else:
          logger.info("Already up to date!")
      else:
        #Ask the user to turn on auto-update #TODO: Usability
        response = swu_interface.ask_first_time()
        config['use_updater'] = response
        self.save_config(config)

    except Exception as e:
      logger.error("Updater Failed")
      logger.error(e)

def check_for_update(queue):
  sys.stdout = WriteStream(queue)
  thread = UpdateThread(queue)
  thread.start()
  return thread


if __name__ == '__main__':
  main()