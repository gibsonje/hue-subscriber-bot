from subprocess import call, check_output
from sys import platform as _platform
import os

if _platform in ("darwin", "linux"):
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

    hooks_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pyinstaller_hooks")

check_output(['pyinstaller',
     'main.py',
     '--additional-hooks-dir={}'.format(hooks_dir),
     '--noconfirm',
     '--name=HueBot',
     '--windowed'
    ] + bonus_args)
