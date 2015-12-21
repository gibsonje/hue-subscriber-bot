import logging
import sys


def get_logger():
  """
  Configure & return a logger.
  :return: logging.Logger
  """
  #### Configure Logger ####
  # Log to stdout
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(message)s',
                                '%m/%d/%Y %H:%M:%S')
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  return logger