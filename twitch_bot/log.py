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

  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(message)s',
                                '%m/%d/%Y %H:%M:%S')
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  logger.info(logger.handlers)

  return logger