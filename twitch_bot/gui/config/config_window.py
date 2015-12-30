from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebView
import os.path
import yaml
from gui import exceptions
from gui.dialog.config_2 import Ui_Dialog
from util import util
from log import get_logger
logger = get_logger(__name__)

class ConfigWindow(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent=None):
    super(ConfigWindow, self).__init__(parent)
    self.setupUi(self)

    self.dialog_buttons.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.save_and_close)
    self.dialog_buttons.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
    self.dialog_buttons.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save)

    self.color_picker_1_btn.clicked.connect(lambda: self.color_window(self.flash_color_1, self.flash_1_web))
    self.color_picker_2_btn.clicked.connect(lambda: self.color_window(self.flash_color_2, self.flash_2_web))

  def color_window(self, color_picker, color_box):
    start_hue = int(color_picker.text())
    start_color = util.hue_qcolor(start_hue)
    color_window = QtGui.QColorDialog(start_color)

    color = color_window.getColor()

    color_picker.setText(str(color.hue() * (int)(float(65535) / 359)))
    self.paint_box(color_box, color.name())

  # Hack
  def field_map(self, field_map={}):

    if not field_map:
      field_map = {
        'username': self.username_text,
        'oauth': self.oauth_text,
        'admin-user': self.username_text,
        'channel': self.channel_text,
        #'hue-bridge-group': self.hue_group_combo,
        'hue-bridge-ip': self.hue_ip_text,
        'hue-color-end': self.flash_color_2,
        'hue-color-start': self.flash_color_1,
        'hue-flash-count': self.hue_flash_count_spin_box,
        'hue-transition-time': self.flash_speed_slider
      }

    return field_map

  def load_config(self):
    """
    Tries to load the config.yml and returns a dictionary.
    :return: dict
    """

    try:
      if os.path.isfile("config.yml"):
        with open("config.yml", 'r') as config_file:
          return yaml.load(config_file) or {}
      else:
        raise exceptions.ConfigLoadFailed("No config file found.")
    except IOError:
      raise exceptions.ConfigLoadFailed("Failed to load yaml config file.")


  def load(self):
    try:
      config = self.load_config()
    except Exception as e:
      #TODO: Error dialog
      return

    for field, field_gui in self.field_map().iteritems():
      if isinstance(field_gui, QtGui.QLineEdit):
        field_gui.setText(str(config[field]))
      elif isinstance(field_gui, (QtGui.QSlider, QtGui.QSpinBox)):
        field_gui.setValue(int(config[field]))
      elif isinstance(field_gui, (QtGui.QComboBox)):
        test = QtGui.QComboBox()
        test.setItemText(0, config[field])
        test.setCurrentIndex(0)
      else:
        raise Exception("WTF")

    self.paint_box(self.flash_1_web, util.hue_to_hex(float(config['hue-color-start']) / float(65535)))
    self.paint_box(self.flash_2_web, util.hue_to_hex(float(config['hue-color-end']) / float(65535)))

  def paint_box(self, box, hex):
    box.setHtml('<html><body style="background-color:{};"/></html>'.format(hex))
    box.show()
    logger.info('<html><body style="background-color:{};"/></html>'.format(hex))

  def save_and_close(self):
    self.save()
    self.close()

  def save(self):
    pass
    #config_file = open('config.yml', 'w+')

  def close(self):
    self.hide()

  def reset(self):
    pass