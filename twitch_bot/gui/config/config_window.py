from PyQt4 import QtGui, QtCore
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

  # Hack
  def field_map(self, field_map={}):

    if not field_map:
      field_map = {
        'username': self.username_text,
        'oauth': self.oauth_text,
        'admin-user': self.username_text,
        'channel': self.channel_text,
        'hue-bridge-group': self.hue_group_combo,
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

    #Special Things
    def paint_box(box, hue):
      logger.info(str(hue))
      hue = util.hue_65535_to_365(hue)
      logger.info(str(hue))

      color = QtGui.QColor.fromHsv(hue, 128, 128)
      logger.info(color)
      brush = QtGui.QBrush()
      brush.setColor(color)
      logger.info(brush)

      scene = QtGui.QGraphicsScene()
      scene.setBackgroundBrush(brush)
      logger.info(scene)

      box.setScene(scene)
      #box.render(QtGui.QPainter())

    paint_box(self.flash_color_1_graphic, config['hue-color-start'])
    paint_box(self.flash_color_2_graphic, config['hue-color-end'])

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