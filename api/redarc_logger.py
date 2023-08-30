import datetime
import logging
import os

def init_logger(name):
   if not os.path.exists('logs'):
      os.makedirs('logs')
   logger = logging.getLogger(name)
   time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
   logging.basicConfig(filename='logs/redarc_api-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)
   return logger