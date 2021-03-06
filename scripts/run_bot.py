"""Usage: run_bot.py [options]

Options:
    --host=HOST  IRC Host [default: irc.twitch.tv].
    --port=PORT  IRC Port [default: 6667].
    --channel=CHANNEL  IRC Channel.
    --username=USERNAME  Twitch Username.
    --oauth=OAUTH  Twitch OAuth Token.
    --admin-user=ADMIN-USER  Twitch Username of Admin.
    --hue-bridge-ip=HUE-BRIDGE-IP  Hue Bridge IP.
    --hue-bridge-group=HUGE-BRIDGE-GROUP  Hue Group Name.
    --hue-color-start=HUE-COLOR-START  Hue Flash Color Start [default: 46920].
    --hue-color-end=HUE-COLOR-END  Hue Flash Color End [default: 65535].
    --hue-transition-time=HUE-TRANSITION-TIME  Hue Flash Hectaseconds[default: 10].
    --hue-flash-count=HUE-FLASH-COUNT  Hue Number of Flashes [default: 3].

"""

from twitch_bot.log import get_logger
from twitch_bot.twitch_hue_bot import TwitchHueBot

import docopt

def main():
  logger = get_logger(__name__)

  try:
    arguments = docopt.docopt(__doc__)

    config = {
      'twitch_host': arguments['--host'],
      'twitch_port': int(arguments['--port']),
      'twitch_channel':  arguments['--channel'],
      'twitch_username': arguments['--username'],
      'twitch_oauth': arguments['--oauth'],
      'admin_user': arguments['--admin-user'],
      'hue_bridge_ip': arguments['--hue-bridge-ip'],
      'hue_bridge_group': arguments['--hue-bridge-group'],
      'hue_color_start': int(arguments['--hue-color-start']),
      'hue_color_end': int(arguments['--hue-color-end']),
      'hue_transition_time': int(arguments['--hue-transition-time']),
      'hue_flash_count': int(arguments['--hue-flash-count'])
    }

    bot = TwitchHueBot(config)
    bot.run()

  except docopt.DocoptExit as e:
    logger.error(e.message)
    exit(1)

if __name__ == '__main__':
  main()
