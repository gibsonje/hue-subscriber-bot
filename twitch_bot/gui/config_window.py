import os.path
import webbrowser

import phue
import yaml
from PyQt4 import QtGui, QtCore

import twitch_bot.twitch_hue_bot as twitch_irc
import twitch_bot.util as util
from twitch_bot.config_schema import AppConfig
from twitch_bot.gui import exceptions
from twitch_bot.gui.forms.config import Ui_Dialog
from twitch_bot.log import get_logger
from twitch_bot.gui.schema_mapper import SchemaMapper

logger = get_logger(__name__)


class ConfigWindow(QtGui.QDialog, Ui_Dialog):
  def __init__(self, parent=None):
    super(ConfigWindow, self).__init__(parent)
    self.setupUi(self)

    self.dialog_buttons.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
    self.dialog_buttons.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save_and_close)

    self.color_picker_1_btn.clicked.connect(lambda: self.color_window('color_start', self.flash_1_web))
    self.color_picker_2_btn.clicked.connect(lambda: self.color_window('color_end', self.flash_2_web))

    self.test_flash_button.clicked.connect(self.test_flash)
    self.test_connection_btn.clicked.connect(self.test_hue_connection)
    self.oauth_btn.clicked.connect(lambda: webbrowser.open("https://twitchapps.com/tmi/"))

    self.hue_ip_text.textChanged.connect(lambda: self.test_flash_button.setEnabled(False))

    self.username_text.textEdited.connect(self.username_edited)

    self.flash_speed_slider.setInvertedAppearance(True)

    # Gui Bindings:
    logger.info("Creating GUI bindings")
    schema_mapper = SchemaMapper(AppConfig)
    schema_mapper.bind("twitch:oauth", self.oauth_text.setText, lambda: str(self.oauth_text.text()))
    schema_mapper.bind("twitch:username", self.username_text.setText, lambda: str(self.username_text.text()).strip())
    schema_mapper.bind("twitch:channel", self.channel_text.setText, lambda: str(self.channel_text.text()).strip())

    schema_mapper.bind("hue:bridge_ip", self.hue_ip_text.setText, lambda: str(self.hue_ip_text.text()).strip())
    def hue_color_set(box, hue_dict):
      hex = util.hue_to_hex(hue_dict.values())
      self.paint_box(box, hex)

    #TODO: Real get
    schema_mapper.bind("hue:color_start",
                       lambda x: hue_color_set(self.flash_1_web, x),
                       lambda: util.hex_to_65535_hue(str(self.flash_1_web.toolTip())))
    schema_mapper.bind("hue:color_end",
                       lambda x: hue_color_set(self.flash_2_web, x),
                       lambda: util.hex_to_65535_hue(str(self.flash_2_web.toolTip())))

    schema_mapper.bind("hue:transition_time", self.flash_speed_slider.setValue, self.flash_speed_slider.value())
    schema_mapper.bind("hue:flash_count", self.hue_flash_count_spin_box.setValue, self.hue_flash_count_spin_box.value())

    self.schema_mapper = schema_mapper


    for x in (self.test_connection_btn_2, self.unlock_channel, self.bridge_detect_btn,
              self.test_flash_button):
      x.setDisabled(True)

  def username_edited(self):
    channel_txt = str(self.channel_text.text())
    username_txt =str(self.username_text.text())

    # Hax
    if  channel_txt == "#{}".format(username_txt.lower()[:-1]) or \
            channel_txt[:-1] == "#{}".format(username_txt.lower()):
      self.channel_text.setText("#{}".format(username_txt.lower()))

  def get_current_config(self):
    hex_1 = str(self.flash_1_web.toolTip())
    hex_2 = str(self.flash_2_web.toolTip())
    config = {
      'twitch': {
        "oauth": str(self.oauth_text.text()).strip(),
        "username": str(self.username_text.text()).strip(),
        "channel": str(self.channel_text.text()).strip(),
      },
      'hue': {
        "bridge_ip": str(self.hue_ip_text.text()).strip(),
        "color_start": util.hex_to_65535_hue(hex_1),
        "color_end": util.hex_to_65535_hue(hex_2),
        "transition_time": int(self.flash_speed_slider.value()) * 10,
        "flash_count": int(self.hue_flash_count_spin_box.value())
      }
    }
    logger.debug(config)
    return config

  def test_hue_connection(self):
    config = self.get_current_config()
    try:
      @util.run_sync
      def run():
        phue.Bridge(config['hue']['bridge_ip'])
      run()
    except Exception as e:
      self.test_flash_button.setEnabled(False)
      logger.info(e.message)
      QtGui.QMessageBox.critical(self, "Failed to Connect", "Failed to connect to Hue Bridge {}".format(config['hue_bridge_ip']))
    else:
      self.test_flash_button.setEnabled(True)
      QtGui.QMessageBox.information(self, "Success", "Successfully connected!")

  def test_flash(self):
    try:
      @util.run_async
      def run():
        self.test_flash_button.setEnabled(False)
        bot = twitch_irc.TwitchHueBot(self.get_current_config())
        bot.trigger_hue()
        self.test_flash_button.setEnabled(True)
      run()
    except:
      QtGui.QMessageBox.critical(self, "Failed", "Bot crashed attempting flashes.")

  def color_window(self, config_field, color_box):
    cfg = self.get_current_config()
    if str(color_picker.text()).strip():
      start_hue = cfg['hue'][config_field]['hue']
      start_color = util.hue_qcolor(start_hue)
    else:
      start_color = QtGui.QColor()
      start_color.setGreen(255)

    color_window = QtGui.QColorDialog(start_color)

    color = color_window.getColor()

    self.paint_box(color_box, color.name())


  def load_config(self):
    """
    Tries to load the config.yml and returns a dictionary.
    :return: dict
    """
    try:
      with open("config.yml", 'r') as config_file:
        raw_config = yaml.load(config_file)
    except IOError as e:
      raw_config = {}

    config = AppConfig.to_python(raw_config)

    return AppConfig.from_python(config)

  def load(self):
    config = self.load_config()
    logger.info("Config Loaded")


    self.schema_mapper.set_bound(config)


  @staticmethod
  def paint_box(box, hex):
    box.setToolTip(QtCore.QString(hex))
    box.setHtml('<html><body style="background-color:{};"/></html>'.format(hex))
    box.show()

  def save_and_close(self):
    self.save()
    self.close()

  def save(self):
    config = {}
    field_map = self.field_map()
    for section_name, section in field_map.iteritems():
      for config_name, field_gui in section.iteritems():
        if isinstance(field_gui, QtGui.QLineEdit):
          config[section_name][config_name] = str(field_gui.text()).strip()
        elif isinstance(field_gui, (QtGui.QSlider, QtGui.QSpinBox)):
          config[section_name][config_name] = int(field_gui.value())

    with open('config.yml', 'w+') as config_file:
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