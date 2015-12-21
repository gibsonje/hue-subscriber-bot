import logging
import sys

def get_logger(name):
  """
  Configure & return a logger.
  :return: logging.Logger
  """
  #### Configure Logger ####
  # Log to stdout
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)

  formatter = logging.Formatter('%(asctime)s - %(message)s',
                                '%m/%d/%Y %H:%M:%S')
  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  return logger