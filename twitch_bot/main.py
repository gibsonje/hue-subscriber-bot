from PyQt4 import QtGui, QtCore
import sys, os
import hue_bot
import config

import subprocess
import yaml

from twitch_irc import TwitchIrc

def resource_path(relative):
  if hasattr(sys, "_MEIPASS"):
    return os.path.join(sys._MEIPASS, relative)
  return os.path.join(relative)

class ConfigWindow(QtGui.QDialog, config.Ui_Dialog):
  def __init__(self, parent=None):
    super(ConfigWindow, self).__init__(parent)
    self.setupUi(self)

    self.button_box.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save)
    self.button_box.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.close)
    self.button_box.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)

    self.load()

  def load(self):
    config = {}
    if os.path.isfile("config.yml"):
      with open("config.yml", 'r') as config_file:
        config = yaml.load(config_file) or {}

    if config:
      if 'username' in config:
        self.username_textbox.setText(config['username'])
      if 'oauth' in config:
        self.oauth_textbox.setText(config['oauth'])
      if 'admin-user' in config:
        self.admin_textbox.setText(config['admin-user'])
      if 'channel' in config:
        self.channel_textbox.setText(config['channel'])
      if 'hue-bridge-group' in config:
        self.hue_group_textbox.setText(config['hue-bridge-group'])
      if 'hue-bridge-ip' in config:
        self.hue_ip_textbox.setText(config['hue-bridge-ip'])
      if 'hue-color-end' in config:
        self.color_end_textbox.setText(str(config['hue-color-end']))
      if 'hue-color-start' in config:
        self.color_start_textbox.setText(str(config['hue-color-start']))
      if 'hue-flash-count' in config:
        self.flash_count_spinner.setValue(config['hue-flash-count'])
      if 'hue-transition-time' in config:
        self.flash_speed_slider.setValue(config['hue-transition-time'])

  def save(self):
    config_file = open('config.yml', 'w+')
    config = yaml.load(config_file) or {}
    config['host'] = "irc.twitch.tv"
    config['port'] = 6667
    config['channel'] = str(self.channel_textbox.text())
    config['username'] = str(self.username_textbox.text())
    config['oauth'] = str(self.oauth_textbox.text())
    config['admin-user'] = str(self.admin_textbox.text())
    config['hue-bridge-ip'] = str(self.hue_ip_textbox.text())
    config['hue-bridge-group'] = str(self.hue_group_textbox.text())
    config['hue-color-start'] = int(str(self.color_start_textbox.text()))
    config['hue-color-end'] = int(str(self.color_end_textbox.text()))
    config['hue-transition-time'] = int(self.flash_speed_slider.value())
    config['hue-flash-count'] = int(self.flash_count_spinner.value())

    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, data: True

    file_contents = yaml.dump(config,
                              default_flow_style=False,
                              Dumper=noalias_dumper)

    config_file.write(file_contents)

  def close(self):
    self.hide()

  def reset(self):
    pass

class MainWindow(QtGui.QMainWindow, hue_bot.Ui_main_window):
  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)
    self.setupUi(self)

    self.config_button.clicked.connect(self.open_config)
    self.start_button.clicked.connect(self.start_bot)

    self.config_gui = ConfigWindow()
    self.config_gui.hide()

  def open_config(self):
    self.config_gui.show()

  def loop(self, time, callback):
    timer = QtCore.QTimer()
    timer.setSingleShot(False)
    timer.timeout.connect(callback)
    timer.start(time)

    return timer

  def update_list(self, line):
    self.text_list.addItem(line)

  class BotThread(QtCore.QThread):
    bot_updated_signal = QtCore.pyqtSignal(str)


    def run(self):
      # FIXME: This is some hackathon level shit right here
      # I spent about 12 hours on a really fancy way to share output
      # with a thread, but it did not bundle with installers well...
      if os.path.isfile("config.yml"):
        with open("config.yml", 'r') as config_file:
          config = yaml.load(config_file) or {}
          snake_config = {k.replace('-','_'): v
                          for k, v in config.iteritems()}
          snake_config['twitch_host'] = snake_config['host']
          snake_config['twitch_port'] = snake_config['port']
          snake_config['twitch_oauth'] = snake_config['oauth']
          snake_config['twitch_username'] = snake_config['username']
          snake_config['twitch_channel'] = snake_config['channel']
          snake_config['hue_transition_time']*=10
          bot = TwitchIrc(snake_config)
          bot.run()


  def start_bot(self):
    app = QtCore.QCoreApplication.instance()
    self.bot_thread = self.BotThread()
    self.bot_thread.finished.connect(app.exit)
    self.bot_thread.bot_updated_signal.connect(self.update_list)
    self.bot_thread.start()


def main():
  app = QtGui.QApplication(sys.argv)
  form = MainWindow()
  form.show()
  app.exec_()

if __name__ == '__main__':
  main()