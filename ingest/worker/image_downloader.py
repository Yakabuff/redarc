import datetime
import logging
import os
import sys
import time
import traceback
from gallery_dl import config, job
from redis import Redis
from rq import Worker
from dotenv import load_dotenv
load_dotenv()

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='logs/img_downloader_worker-'+time_now+'.log', encoding='utf-8', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

try:
   redis_conn = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
except Exception as error:
   logging.error(traceback.format_exc())
   logging.error(error)
   sys.exit(1)

def download_image(url, subreddit):
   time.sleep(5)
   if not os.path.exists('gallery-dl'):
      os.makedirs('gallery-dl')
   config.load()  # load default config files
   config.set(("extractor",), "base-directory", "gallery-dl")
   config.set(("extractor",), "directory", [subreddit])

   if job.DownloadJob(url).run() != 0:
      logging.error(f'Failed to download image:{url} subreddit: {subreddit}')
   else:
      logging.info(f'Download images:{url} subreddit: {subreddit}')

if __name__ == "__main__":
    logging.info("Starting image_downloader_worker")
    try:
        w = Worker(['img_urls'], connection=redis_conn, log_job_description=False)
        w.work(logging_level=logging.WARNING)
    except Exception as error:
        logging.error(traceback.format_exc())
        logging.error(error)