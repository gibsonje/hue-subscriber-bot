import re
import socket
from phue import Bridge, Group
from time import sleep

from log import get_logger

TWITCH_IRC_HOST = "irc.twitch.tv"
TWITCH_IRC_PORT = 6667


class TwitchHueBot:
  def __init__(self, config):
    self.config = config
    self.logger = get_logger(self.__class__.__name__)

  @classmethod
  def light_state(cls, lights):
    state = {}

    for light in lights:
      state[light.light_id] = (light.hue, light.saturation, light.brightness)

    return state

  @staticmethod
  def all_lights_group(bridge, logger):
    group_name = 'color_lights'
    try:
      group = Group(bridge, group_name)
      return group
    except (TypeError, LookupError) as e:
      logger.info("Creating a new group called '%s' with all color-enabled lights.", group_name)

    colorable_lights = []
    for light in bridge.lights:
      try:
        colorable_lights.append(light)
      except KeyError as error:
        # Lux light, doesn't support color.
        logger.debug("Light %s doesn't support color.", light.light_id)
        pass

    colorable_ids = [ str(light.light_id) for light in colorable_lights ]
    logger.debug("All Color Lights: %s", ', '.join(colorable_ids))
    bridge.create_group(group_name, colorable_ids)

    return Group(bridge, group_name)

  @classmethod
  def set_state(cls, bridge, state):
    for light, hue in state.iteritems():
      bridge.set_light(light, {'hue': hue[0],
                               'sat': hue[1],
                                'bri': hue[2]})

  def trigger_hue(self):
    self.logger.info("Triggering Hue Flash")
    hue_bridge_ip = self.config['hue']['bridge_ip']
    self.logger.debug("Connecting to Hue Bridge")
    b = self.connect_hue_bridge(hue_bridge_ip)
    api_result = b.get_api()
    self.logger.debug("Connected to Hue Bridge")
    self.logger.debug("*** Hue Debug Info: ***")
    self.logger.debug(api_result)

    names = [v.get('name','NO NAME') for k,v in api_result['groups'].iteritems()]
    msg = "Groups found: {}".format(str(names))
    self.logger.debug(msg)

    try:
      # Try to load the configured group
      group = Group(b, self.config['hue_bridge_group'])
      group_id = group.group_id
    except (TypeError, LookupError) as e:
      # Group not found, use all color enabled lights.
      self.logger.error("Couldn't load the configured group, using all color-enabled lights.")
      try:
        group = TwitchHueBot.all_lights_group(b, self.logger)
        group_id = group.group_id
      except (TypeError, LookupError) as e:
        self.logger.error("Failed to connect to backup group.")
        raise e
    else:
      self.logger.debug("~*** Successfully connected to Hue Group! ***~")

    self.logger.debug("Saving current light state.")
    prev_state = self.light_state(group.lights)

    color_start = self.config['hue']['color_start']
    color_end = self.config['hue']['color_end']
    transition_time = self.config['hue']['transition_time']

    def build_config(hue_dict):
      return {'hue': hue_dict['hue'],
              'sat': hue_dict['saturation'],
              'bri': hue_dict['value']}

    c1 = build_config(color_start)
    c2 = build_config(color_end)

    self.logger.debug("Beginning flashes.")
    b.set_group(group_id, c1)
    for x in range(self.config['hue']['flash_count']):
      b.set_group(group_id, c2, transitiontime=transition_time*10)
      sleep(transition_time)
      b.set_group(group_id, c1, transitiontime=transition_time*10)
      sleep(transition_time)

    self.logger.debug("Resetting lights to previous state.")
    self.set_state(b, prev_state)

  @classmethod
  def connect_hue_bridge(cls, hue_bridge_ip):
    b = Bridge(hue_bridge_ip)

    return b

  @classmethod
  def send_pong(cls, con, msg):
      con.send(bytes('PONG %s\r\n' % msg))

  @classmethod
  def send_message(cls, con, chan, msg):
      con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg)))

  @classmethod
  def send_nick(cls, con, nick):
      con.send(bytes('NICK %s\r\n' % nick))

  @classmethod
  def send_pass(cls, con, password):
      con.send(bytes('PASS %s\r\n' % password))


  @classmethod
  def join_channel(cls, con, chan):
      con.send(bytes('JOIN %s\r\n' % chan))

  @classmethod
  def part_channel(cls, con, chan):
      con.send(bytes('PART %s\r\n' % chan))

  @classmethod
  def get_sender(cls, msg):
    result = ""
    for char in msg:
      if char == "!":
          break
      if char != ":":
          result += char
    return result

  @classmethod
  def get_message(cls, msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
      result += msg[i] + " "
      i += 1
    result = result.lstrip(':')
    return result

# --------------------------------------------- End Command Functions ----------------------------------------------

  def run(self):

    b = self.connect_hue_bridge(self.config['hue']['bridge_ip'])
    b.connect()
    b.get_api()

    con = socket.socket()
    con.connect((TWITCH_IRC_HOST, TWITCH_IRC_PORT))

    self.send_pass(con, self.config['twitch']['oauth'])
    self.send_nick(con, self.config['twitch']['username'])
    self.join_channel(con, self.config['twitch']['channel'])

    self.logger.info("Connected to chat.")

    data = ""

    while True:
      try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
          line = line.encode()
          line = str.rstrip(line)
          line = str.split(line)

          if len(line) >= 1:
            if line[0] == 'PING':
              self.send_pong(con, line[1])

            if line[1] == 'PRIVMSG':
              sender = self.get_sender(line[0]).strip()
              message = self.get_message(line)

              if sender.strip().lower() == "twitchnotify":
                if 'subscribed' in message.strip().lower():
                  self.trigger_hue()

              if sender.strip().lower() in self.config['twitch']['admins'].lower():
                if message.strip().lower() == "hue":
                  self.logger.info("Admin user triggered an event.")
                  self.trigger_hue()

              #self.logger.debug(sender + ": " + message)
      except UnicodeEncodeError:
        pass

      except socket.error:
        self.logger.error("Socket died")

      except socket.timeout:
        self.logger.error("Socket timeout")

      except Exception as e:
        self.logger.debug("**** UNEXPECTED ERROR ****")
        self.logger.error(type(e))
        self.logger.error(e.message)