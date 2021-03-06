from PyQt4 import QtGui
from colorsys import hsv_to_rgb, rgb_to_hsv
import re
from Queue import Queue, Empty
import sys


def hue_65535_to_365(val_65535):
  ratio = float(val_65535) / float(65535)
  val_359 = int(359 * ratio)

  return val_359

def hue_359_to_65535(val_359):
  ratio = float(val_359) / float(359)
  val_65535 = int(65535 * ratio)

  return val_65535


def hue_qcolor(hue_color):
  hue = float(hue_color['hue']) / float(65535)
  return QtGui.QColor.fromHsv(hue, hue_color['saturation'], hue_color['value'])


def hue_to_rgb(hue):
  """
  :type hue: tuple
  :param hue: Phillip's Hue (h<65535>,s<255>,v<255>)
  :return: tuple: r<255>,g<255>,b<255>
  """
  hsv_to_rgb_res = hsv_to_rgb(float(hue[0]) / 65535.0,
                              float(hue[1]) / 255.0,
                              float(hue[2]) / 255.0)

  return map(lambda x: int(x * 255), hsv_to_rgb_res)

def hue_to_hex(hue):
  rgb = hue_to_rgb(hue)

  return rgb_to_hex(hue_to_rgb(hue))

def hex_to_65535_hue(hex):
  assert isinstance(hex, str)
  assert "#" in hex
  assert len(hex) == 7

  qcolor = hex_to_qcolor(hex)
  hue_359 = qcolor.hue()
  hue_65535 = hue_359_to_65535(hue_359)
  sat = qcolor.saturation()
  val = qcolor.value()

  return {'hue': hue_65535, 'saturation': sat, 'value': val}

def rgb_to_hex(rgb):
  converted = map(lambda x: str(hex(x))[2:].zfill(2), rgb)

  return "#%s%s%s" % tuple(converted)


def hex_to_rgb(hex):
  """
  assumes hexs string #FFFFFF
  """
  split = re.findall('..', hex[1:])

  return tuple(int('0x{}'.format(x), 16) for x in split)


def rgb_to_255_hsv(rgb):
  ratio_rgb = [float(x) / 255.0 for x in rgb]

  return rgb_to_hsv(*ratio_rgb)


def hex_to_qcolor(hex_str):
  rgb = hex_to_rgb(hex_str)

  qcolor = QtGui.QColor.fromRgb(*rgb)

  return qcolor

def run_async(func):
  """
  run_async(func)
  function decorator, intended to make "func" run in a separate
  thread (asynchronously).
  Returns the created Thread object

  E.g.:
  @run_async
  def task1():
      do_something

  @run_async
  def task2():
      do_something_too

  t1 = task1()
  t2 = task2()
  ...
  t1.join()t2.join()
  """
  from threading import Thread
  from functools import wraps
  from multiprocessing import Process


  @wraps(func)
  def async_func(*args, **kwargs):
    func_hl = Thread(target=func, args=args, kwargs=kwargs)
    func_hl.start()
    return func_hl

  return async_func



def run_sync(func):
  """
  run_async(func)
  function decorator, intended to make "func" run in a separate
  thread (asynchronously).
  Returns the created Thread object

  E.g.:
  @run_async
  def task1():
      do_something

  @run_async
  def task2():
      do_something_too

  t1 = task1()
  t2 = task2()
  ...
  t1.join()t2.join()
  """
  from threading import Thread
  from functools import wraps
  from multiprocessing import Process

  class ExcThread(Thread):
    def __init__(self, bucket, func, func_args, func_kwargs, *args, **kwargs):
      super(ExcThread, self).__init__(*args, **kwargs)
      self.bucket = bucket
      self.to_run = (func, func_args, func_kwargs)

    def run(self):
      try:
        self.to_run[0](*self.to_run[1], **self.to_run[2])
      except Exception:
        exctype, value = sys.exc_info()[:2]
        self.bucket.put((exctype, value))

  @wraps(func)
  def sync_func(*args, **kwargs):
    bucket = Queue()
    func_hl = ExcThread(bucket, func, args, kwargs)
    func_hl.start()
    while True:
      try:
        exc_type, exc_value = bucket.get(block=False)
        # deal with the exception
        raise exc_type(exc_value)
      except Empty:
        pass

      func_hl.join(0.1)
      if func_hl.isAlive():
        continue
      else:
        try:
          exc_type, exc_value = bucket.get(block=False)
          # deal with the exception
          raise exc_type(exc_value)
        except Empty:
          pass
        break

    return func_hl

  return sync_func



if __name__ == "__main__":

  test = hex_to_65535_hue("#FF00FF")
  print test