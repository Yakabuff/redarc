"""
Fetches URLS from threads from a specified subreddit that match a certain pattern and downloads 
1) Query # of threads before timestamp from database
2) Run gallery-dl on url
"""

import logging
import sys
import time
from psycopg2 import pool
import psycopg2
import os
from dotenv import load_dotenv
from gallery_dl import config, job
load_dotenv()

subreddit = sys.argv[1]
after_timestamp = sys.argv[2]
number = sys.argv[3]
text = "select url from submissions where subreddit=%s and created_utc > %s ORDER BY created_utc ASC LIMIT %s"

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

try:

   pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                      password=os.getenv('PG_PASSWORD'),
                                                      host=os.getenv('PG_HOST'),
                                                      port=os.getenv('PG_PORT'),
                                                      database=os.getenv('PG_DATABASE'))
   pg_con = pg_pool.getconn()
   cursor = pg_con.cursor()
   cursor.execute(text, [subreddit, after_timestamp, number])
   comments = cursor.fetchall()
   for i in comments:
      if 'i.redd.it' in i[0]:
         download_image(i[0], subreddit)
except Exception as error:
   print(error)


