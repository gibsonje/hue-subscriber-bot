hue-subscriber-bot
====================
An IRC monitoring bot that flashes your Hue lights when somebody subscribes to a specified channel.

Download a Windows Executable here:
https://github.com/gibsonje/hue-subscriber-bot/releases

Run the file *"main.exe"* and click Configure.

Example Configuration:
  * **Twitch Username:** ImCoty
  * **Twitch Channel:** #imcoty *('#' followed by lowercase username)*
  * **OAuth Token:** Generate yours here: http://www.twitchapps.com/tmi/
  * **Admin Username:** ImCoty *(This user can trigger your lights to flash by typing "hue" into Twitch chat.)*
  * **Hue Bridge IP:** IP of your Hue Bridge. You can get this within the Hue app. //TODO: Explain how.
  * **Hue Group Name:** You must make a group in the hue app with a name. These are the bulbs that will flash. //TODO: Explain how

You should leave Flash Speed and other options at their defaults for the first run.

BEFORE RUNNING
==============
Press the button on the Hue Bridge before you hit "Start Bot"

If everything works you'll start to see the Twitch chat in the bot's window. You can test that the Hue lights are working by typing "hue" into your chat.
