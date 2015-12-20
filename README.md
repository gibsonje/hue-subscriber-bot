# hue-subscriber-bot
A bot for flashing your hue bulbs when you get a subscriber.

## Running on Windows


Download and install Python 2:
https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

1. Open powershell and copy&paste(right click) this:

`[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")`

2. Download get-pip.py here: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
3. Doubleclick to install it
4. Open a command prompt and type "pip install phue"

Now download run.py, change all relevant settings, and double click it.

The first time you run this you will need to hit your hue bridge's search button within 30 seconds of running it.
