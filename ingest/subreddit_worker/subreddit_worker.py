import hashlib
from logging.handlers import RotatingFileHandler
import sys
from redis import Redis
import logging
import time
import praw
import time
from rq.job import JobStatus
import os
from rq import Queue
from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
load_dotenv()

"""
Subreddit worker
1) Fetch subreddit list from envar: split string by comma
2) Every x minutes, for each subreddit, fetch rising, new
3) Add thread ids into queue for processing
4) Deduplicate threads to minimize number of requests and do not add thread that already exists in queue
https://stackoverflow.com/questions/70970403/how-to-check-if-a-similar-scheduled-job-exists-in-python-rq
Set jobid as hash of thread id and check if jobid exists
"""

if not os.path.exists('logs'):
   os.makedirs('logs')
filename = 'logs/subreddit_worker.log'
handler = RotatingFileHandler(filename,
                           maxBytes=1024*1024*50,
                           backupCount=5)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                     encoding='utf-8',
                     level=logging.INFO,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     handlers=[handler])

try:
   reddit = praw.Reddit(
      client_id=os.getenv('CLIENT_ID'),
      client_secret=os.getenv('CLIENT_SECRET'),
      password=os.getenv('PASSWORD'),
      user_agent=os.getenv('USER_AGENT'),
      username=os.getenv('REDDIT_USERNAME'),
   )
   pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                         password=os.getenv('PG_PASSWORD'),
                                                         host=os.getenv('PG_HOST'),
                                                         port=os.getenv('PG_PORT'),
                                                         database=os.getenv('PG_DATABASE'))
   redis_conn = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

   url_queue = Queue("url_submit", connection=redis_conn)
except Exception as error:
    logging.error(error)
    sys.exit(1)

def watch_subreddit(subreddit):
   # Get intersection of new posts and rising posts and hot posts
   # Insert ids into a set
   ids = {}
   hot = reddit.subreddit(subreddit).hot(limit=int(os.getenv('NUM_THREADS')))
   for h in hot:
      id = hashlib.md5(h.id.encode('utf-8')).hexdigest() 
      if not id in ids:
         ids[id] = (h.id, h.permalink)

   new = reddit.subreddit(subreddit).new(limit=int(os.getenv('NUM_THREADS')))
   for n in new:
      id = hashlib.md5(n.id.encode('utf-8')).hexdigest() 
      if not id in ids:
         ids[id] = (n.id, n.permalink)

   rising = reddit.subreddit(subreddit).rising(limit=int(os.getenv('NUM_THREADS')))
   for r in rising:
      id = hashlib.md5(r.id.encode('utf-8')).hexdigest() 
      if not id in ids:
         ids[id] = (r.id, r.permalink)
   return ids

def work():
   subreddits = fetch_subreddits()
   for i in subreddits:
      id_set = watch_subreddit(i)
      for i in id_set:
         id = id_set[i][0]
         url = id_set[i][1]
         try:
            if not job_exists(id):
               logging.info("Queuing thread id "+ id)
               job = url_queue.enqueue('reddit_worker.fetch_thread', thread_id=id, url=url, job_id=i)
               if job.get_status(refresh=True) != "queued":
                  logging.error(f"Failed to enqueue job: thread ID {id}")
         except Exception as error:
            logging.error(f"Failed to enqueue job: thread ID {id}")
            logging.error(error)

def job_exists(id):
   job = url_queue.fetch_job(id)  
   if job == None:
      return False
   status = job.get_status()
   if status in {JobStatus.QUEUED, JobStatus.SCHEDULED}:
      # Job exists and will be run.
      return True
   return False

def fetch_subreddits():
   try:
      pg_con = pg_pool.getconn()
      cursor = pg_con.cursor()
      cursor.execute('SELECT * FROM watch')
      pg_pool.putconn(pg_con)
      submissions = cursor.fetchall()
   except Exception as error:
      raise Exception(error) from None
   
   return [i[0] for i in submissions]

if __name__ == "__main__":
   logging.info("Starting subreddit_worker")
   try:
      while True:
         work()
         time.sleep(int(os.getenv('FETCH_DELAY')))
   except Exception as error:
        logging.error(error)