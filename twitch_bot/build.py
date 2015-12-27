from subprocess import call
from sys import platform as _platform

call(['rm',
      '-r',
      'build'])
call(['rm',
      '-r',
      'dist'])
call(['rm',
      '*.pyc'])

bonus_args = []
if "linux" in _platform:
  # linux
  pass
elif _platform == "darwin":
  # OS X
  bonus_args.append("--onedir")
elif _platform == "win32":
  # Windows...
  bonus_args.append("--onefile")

call(['pyinstaller',
     'main.py',
     '--hidden-import=pyinstaller_hooks',
     '--noconfirm',
     '--name=HueBot',
     '--windowed'] + bonus_args)