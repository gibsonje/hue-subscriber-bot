from PyQt4 import QtGui, QtCore
import sys, os
import hue_bot
import config

import subprocess
import yaml

class ConfigWindow(QtGui.QDialog, config.Ui_Dialog):
  def __init__(self, parent=None):
    super(ConfigWindow, self).__init__(parent)
    self.setupUi(self)

    self.button_box.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save)
    self.button_box.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.close)
    self.button_box.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)

    #self.config_button.clicked.connect(self.athing)
    file = open('config.yml', 'w+')
    current_config = yaml.load(file)
    print current_config
    #current_config.set_default("")

  def save(self):
    config = yaml.load(open('config.yml', 'w+')) or {}
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
    config['hue-transition-time'] = self.flash_speed_slider.tickPosition()
    config['hue-flash-count'] = self.flash_count_spinner.value()

    print config

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
      base_path = os.path.dirname(os.path.realpath(__file__))
      path = os.path.join(base_path,"..","run_bot.py")
      command = "python {} {}".format(path,"--username=RoflMyPancakes --oauth=\"oauth:chexhqpdnw08v0p433qkttaefk26ki\" --channel=\"#roflmypancakes\" --admin-user=RoflMyPancakes --hue-bridge-ip=\"192.168.3.129\" --hue-bridge-group=Inside")

      proc = subprocess.Popen(command,
                       shell=True,
                       stdout=subprocess.PIPE,
                       )

      lines_iterator = iter(proc.stdout.readline, b"")
      for line in lines_iterator:
        if line:
          self.bot_updated_signal.emit(str(line))


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