from PyQt4 import QtGui, QtCore
import sys, os
import hue_bot
import config

import subprocess

class ConfigWindow(QtGui.QDialog, config.Ui_Dialog):
  def __init__(self, parent=None):
    super(ConfigWindow, self).__init__(parent)
    self.setupUi(self)

    #self.config_button.clicked.connect(self.athing)

  def athing(self):
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

  def update_list(self):
    while self.proc.poll() is None:
      output = proc.stdout.readline()
      self.text_list.addItem(output)

  def start_bot(self):
    os.path.dirname(os.path.realpath(__file__))

    self.proc = subprocess.Popen('ping google.com',
                       shell=True,
                       stdout=subprocess.PIPE,
                       )

    self.loop(1000,self.update_list)

def main():
  app = QtGui.QApplication(sys.argv)
  form = MainWindow()
  form.show()
  app.exec_()

if __name__ == '__main__':
  main()