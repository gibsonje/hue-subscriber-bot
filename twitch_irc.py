from log import get_logger

import re
import socket
from phue import Bridge, Group
from time import sleep

logger = get_logger()

class TwitchIrc:
  def __init__(self, config):
    self.config = config

  @classmethod
  def light_state(cls, lights):
    state = {}

    for light in lights:
      state[light.light_id] = light.hue

    return state

  @classmethod
  def set_state(cls, bridge, state):
    for light, hue in state.iteritems():
      bridge.set_light(light, 'hue', hue)

  def trigger_hue(self):
    logger.info("Triggering Hue Flash")
    hue_bridge_ip = self.config['hue_bridge_ip']
    b = self.connect_hue_bridge(hue_bridge_ip)


    group = Group(b, self.config['hue_bridge_group'])
    group_id = group.group_id

    prev_state = self.light_state(group.lights)

    color_start = self.config['hue_color_start']
    color_end = self.config['hue_color_end']
    transition_time = self.config['hue_transition_time']

    b.set_group(group_id, {'hue': color_start})
    for x in range(self.config['hue_flash_count']):
      b.set_group(group_id, {'hue': color_end}, transitiontime=transition_time)
      sleep(transition_time / 10)
      b.set_group(group_id, {'hue': color_start}, transitiontime=transition_time)
      sleep(transition_time / 10)

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

  #@classmethod
  #def parse_message(cls, msg):
  #    if len(msg) >= 1:
  #        msg = msg.split(' ')
  #        options = {'!test': command_test,
  #                   '!asdf': command_asdf}
  #        if msg[0] in options:
  #            options[msg[0]]()

# --------------------------------------------- End Command Functions ----------------------------------------------

  def run(self):
    b = self.connect_hue_bridge(self.config['hue_bridge_ip'])
    b.connect()
    b.get_api()

    con = socket.socket()
    con.connect((self.config['twitch_host'], self.config['twitch_port']))

    self.send_pass(con, self.config['twitch_oauth'])
    self.send_nick(con, self.config['twitch_username'])
    self.join_channel(con, self.config['twitch_channel'])

    logger.info("Connected to chat.")

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

              if sender.strip().lower() == self.config['admin_user'].lower():
                if message.strip().lower() == "hue":
                  logger.info("Admin user triggered an event.")
                  self.trigger_hue()

              logger.debug(sender + ": " + message)
      except UnicodeEncodeError:
        pass

      except socket.error:
        logger.error("Socket died")

      except socket.timeout:
        logger.error("Socket timeout")