# hue-subscirber-bot
A bot for flashing your hue bulbs when you get a subscriber.

## Running on Windows


Download the Python 2:
https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

Install easy_setup via this python script:

* Run powershell (start-> type "powershell" in search)
* Copy & paste (right click is paste) each step: 

1. [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")
2. (New-Object Net.WebClient).DownloadFile('https://raw.github.com/pypa/pip/master/contrib/get-pip.pyy', 'get-pip.py')
3. python get-pip.py
4. pip install phue

Now in cmd or powershell, doesn't matter, download the script and run it. Make sure to change all relevant config
* python run.py


