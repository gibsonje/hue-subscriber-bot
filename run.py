#!/usr/bin/env python3

import re
import socket

from phue import Bridge, Group
from time import sleep

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"       # Hostname of the IRC-Server in this case twitch's
PORT = 6667                  # Default IRC-Port
CHAN = "#USERNAME_HERE"      # Channelname = #{Nickname}
NICK = "USERNAME_HERE"       # Nickname = Twitch username
PASS = "OAUTH_KEY_HERE"      # www.twitchapps.com/tmi/ will help to retrieve the required authkey

HUE_BRIDGE_IP = "192.168.1.1"
HUE_TRIGGER_GROUP = "Inside"

COLOR_START = 46920
COLOR_END = 65535

FLASH_TIMES = 3
TRANSITION_TIME = 10 # between 10 and 50ish, experiment, hectaseconds.

# Admin users can trigger a test flash by typing "hue" into chat.
ADMIN_USERS = ['USERNAME_HERE']

# --------------------------------------------- End Settings -------------------------------------------------------
################
# There should be no need to change the code below as a novice user.
################
#
def light_state(lights):
  state = {}

  for light in lights:
    state[light.light_id] = light.hue

  return state

def set_state(bridge, state):
  for light, hue in state.iteritems():
    bridge.set_light(light, 'hue', hue)

def trigger_hue():
  b = Bridge(HUE_BRIDGE_IP)

  # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
  b.connect()

  # Get the bridge state (This returns the full dictionary that you can explore)
  b.get_api()

  group = Group(b, HUE_TRIGGER_GROUP)
  group_id = group.group_id

  prev_state = light_state(group.lights)

  b.set_group(group_id, {'hue': COLOR_START})
  for x in range(FLASH_TIMES):
    b.set_group(group_id, {'hue': COLOR_END}, transitiontime=TRANSITION_TIME)
    sleep(TRANSITION_TIME / 10)
    b.set_group(group_id, {'hue': COLOR_START}, transitiontime=TRANSITION_TIME)
    sleep(TRANSITION_TIME / 10)

  set_state(b, prev_state)
#

# --------------------------------------------- Start Functions ----------------------------------------------------
def connect_hue_bridge():
  b = Bridge(HUE_BRIDGE_IP)
  # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
  b.connect()

def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg)))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!asdf': command_asdf}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, 'testing some stuff')


def command_asdf():
    send_message(CHAN, 'asdfster')
# --------------------------------------------- End Command Functions ----------------------------------------------
connect_hue_bridge()

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

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
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0]).strip()
                    message = get_message(line)
                    parse_message(message)

                    if sender.strip().lower() == "twitchnotify":
                      if 'subscribed' in message.strip().lower():
                        trigger_hue()

                    if sender.strip().lower() in ADMIN_USERS:
                      if message.strip().lower() == "hue":
                        trigger_hue()

                    print(sender + ": " + message)
    except UnicodeEncodeError:
        print "Failed to parse a message"

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")