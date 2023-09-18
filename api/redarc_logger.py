import logging
from logging.handlers import RotatingFileHandler
import os

def init_logger(name):
   if not os.path.exists('logs'):
      os.makedirs('logs')
   logger = logging.getLogger(name)
   filename ='logs/redarc_api.log'
   handler = RotatingFileHandler(filename,
                              maxBytes=1024*1024*50,
                              backupCount=999)
   logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        encoding='utf-8',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[handler])
   return logger