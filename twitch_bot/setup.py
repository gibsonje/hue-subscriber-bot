from sys import platform

if False: #platform == 'win32':
  try:
    try:
      import py2exe.mf as modulefinder
    except ImportError:
      import modulefinder

    import win32com, sys
    for p in win32com.__path__[1:]:
      modulefinder.AddPackagePath("win32com", p)
    for extra in ["win32com.shell"]: #,"win32com.mapi"
      __import__(extra)
      m = sys.modules[extra]
      for p in m.__path__[1:]:
        modulefinder.AddPackagePath(extra, p)
  except ImportError:
    # no build path setup, no worries.
    pass

  import py2exe
  from win32com import storagecon
  from win32com.shell import shell, shellcon