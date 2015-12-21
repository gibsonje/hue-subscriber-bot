# hue-subscriber-bot
A bot for flashing your hue bulbs when you or a channel you're interested in get a subscriber. 

Download here:
https://github.com/gibsonje/hue-subscriber-bot/releases

Run the app and click Configure.

Example Configuration:
Twitch Username: ImCoty
Twitch Channel: #imcoty (# followed by lowercase username)
OAuth Token: Generate yours here: http://www.twitchapps.com/tmi/
Admin Username: ImCoty (this is the user who can trigger a test flash via by typing "hue" into twitch chat)
Hue Bridge IP: IP of your Hue Bridge, obtainable from the app.
Hue Group Name: You must make a group in the hue app with a name. These are the bulbs that will flash.

Flash speed and other options should not be altered on your first run. Play with them later, but first ensure a successful run.

** BEFORE RUNNING **
Once your configuration is saved you must press the button on your Hue Bridge within 30 seconds prior to hitting "Start Bot".

Once the bot is running it will echo all chat into the event list. Try typing into your Twitch channel and verify that you see the message in the bot. Try typing "hue" and see if it properly flashes your lights. 
