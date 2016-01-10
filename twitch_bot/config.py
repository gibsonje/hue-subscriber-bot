import formencode
from formencode import Schema, validators


class TwitchConfig(Schema):
  oauth = validators.String(if_missing="") # TODO: Validate oauth token
  username = validators.String(if_missing="")
  channel = validators.String(if_missing="") # TODO: Validate starts with #
  admins = formencode.ForEach(validators.String(if_missing=""))

class PhillipsHueColor(Schema):

  def __init__(self, default_hue, *args, **kwargs):
    super(PhillipsHueColor, self).__init__(*args, **kwargs)
    self.add_field('hue', validators.Int(min=0, max=65535, if_missing=default_hue))

  saturation = validators.Int(min=0, max=255, if_missing=255)
  value = validators.Int(min=0, max=255, if_missing=255)

class HueConfig(Schema):
  bridge_ip = validators.IPAddress(if_missing="")
  color_start = PhillipsHueColor(65535, if_missing={'hue': 65535, 'saturatin': 255, 'value': 255})
  color_end = PhillipsHueColor(46920, if_missing={'hue': 46920, 'saturatin': 255, 'value': 255})
  transition_time = validators.Int(if_missing=1)
  flash_count = validators.Int(if_missing=3)
  oauth = validators.String() # TODO: Validate oauth token
  username = validators.String()
  channel = validators.String() # TODO: Validate starts with #
  admins = formencode.ForEach(validators.String())

class AppConfig(Schema):
  twitch = TwitchConfig
  hue = HueConfig
