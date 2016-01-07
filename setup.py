from setuptools import setup

import twitch_bot.version as version

setup(
    name='Twitch Hue Bot',
    version=version.package_version,
    description='Connect to Twitch IRC and flash Hue lights on a subscription.',
    author='John Gibson',
    author_email='devgibsonje@gmail.com',
    packages=['twitch_bot'],
    url='https://github.com/gibsonje/hue-subscriber-bot',
)
