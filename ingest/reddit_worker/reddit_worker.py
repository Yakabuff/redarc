import datetime
import sys
import traceback
from redis import Redis
import logging
from validate import validate_submission, validate_comment
import time
import praw
from enum import Enum
import time
from rq import Worker
from rq import get_current_job
from rq import Queue
import os
from psycopg2 import pool
import psycopg2
from dotenv import load_dotenv
load_dotenv()

"""
Redarc worker

1) Make reddit request
2) Insert into DB if comment/submission ID does not exist.  If exist, update gilded, upvotes if number higher.  Update score
"""

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='logs/reddit_worker-'+time_now+'.log', encoding='utf-8', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

try:
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        password=os.getenv('PASSWORD'),
        user_agent=os.getenv('USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
    )

    redis_conn = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    img_queue = Queue("img_urls", connection=redis_conn)
    pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                            password=os.getenv('PG_PASSWORD'),
                                                            host=os.getenv('PG_HOST'),
                                                            port=os.getenv('PG_PORT'),
                                                            database=os.getenv('PG_DATABASE'))
except Exception as error:
    logging.error(traceback.format_exc())
    logging.error(error)
    sys.exit(1)

class type(Enum):
    SUBMISSION = 1
    COMMENT = 2

def progress_start(job_id, url):
    try:
        pg_con = pg_pool.getconn()
        cursor = pg_con.cursor()
        cursor.execute('INSERT INTO progress(job_id, url, start_utc, finish_utc, error) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (job_id) DO NOTHING',
                        [job_id, url, int(time.time()), None, False])
        pg_con.commit()
        pg_pool.putconn(pg_con)
    except Exception as error:
        raise Exception(error) from None

def progress_finish(job_id, error):
    try:
        pg_con = pg_pool.getconn()
        cursor = pg_con.cursor()
        cursor.execute('UPDATE progress SET finish_utc=%s, error=%s where job_id =%s',
                                [int(time.time()), error, job_id])
        pg_con.commit()
        pg_pool.putconn(pg_con)
    except Exception as error:
        raise Exception(error) from None

def fetch_thread(thread_id, url):
    job = get_current_job()
    if job == None:
        raise Exception("Could not get current job") from None
    try:
        logging.debug('Current job: %s' % (job.id,))
        progress_start(job.id, url)
        logging.info("Fetching submission ID: "+ str(thread_id) + " URL: " + str(url))
        submission = reddit.submission(id=thread_id)
        process_submission(submission)
        comments = submission.comments
        comments.replace_more(limit=None)
        for comment in comments.list():
            process_comment(comment)
    except Exception as error:
        logging.error(error)
        logging.error(traceback.format_exc())
        try:
            progress_finish(job.id, True)
        except Exception as error:
            raise Exception(error) from None
    else:
        try:
            progress_finish(job.id, False)
        except Exception as error:
            raise Exception(error) from None

def process_submission(submission):
    x = validate_submission(submission)
    logging.debug("Processing submission: " + x['id'])
    if x != None:
        try:
            if 'i.redd.it' in x['url'] and os.getenv('DOWNLOAD_IMAGES') == 'true':
                job = img_queue.enqueue('image_downloader.download_image', subreddit=x['subreddit'], url=x['url'])
                if job.get_status(refresh=True) != "queued":
                    logging.error(f"Failed to enqueue image url: {x['url']} thread url: {x['permalink']}")
                else:
                    logging.info(f"Queued image url: {x['url']} thread url: {x['permalink']}")
            insert_db(type.SUBMISSION, x)
        except Exception as error:
            raise Exception(error) from None

def process_comment(comment):
    x = validate_comment(comment)
    logging.debug("Processing comments: " + x['id'])
    if x != None:
        try:
            insert_db(type.COMMENT, x)
        except Exception as error:
            raise Exception(error) from None

def insert_db(_type, data):
    try:
        pg_con = pg_pool.getconn()
        # Update score, get max of gilded, get max of num_comments
        cursor = pg_con.cursor()
        if _type == type.SUBMISSION:
            cursor.execute('''INSERT INTO submissions(id, subreddit, title, author, permalink,
                thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self, retrieved_utc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING''',
                [data['id'], data['subreddit'], data['title'], data['author'], data['permalink'], data['thumbnail'],
                data['num_comments'], data['url'], data['score'], data['gilded'], data['created_utc'], data['selftext'], data['is_self'], int(time.time())])
            
            cursor.execute('UPDATE submissions SET num_comments=GREATEST(num_comments, %s), gilded=GREATEST(gilded, %s), score=%s where id =%s',
                            [data['num_comments'], data['gilded'], data['score'], data['id']])

        else:
            cursor.execute('''INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id, retrieved_utc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING''',
                [data['id'], data['subreddit'], data['body'], data['author'], data['score'], data['gilded'],
                data['created_utc'], data['parent_id'], data['link_id'], int(time.time())])

            cursor.execute('UPDATE comments SET gilded=GREATEST(gilded, %s), score=%s where id =%s',
                            [data['gilded'], data['score'], data['id']])
        
        pg_con.commit()
        pg_pool.putconn(pg_con)
    except Exception as error:
        logging.error("Failed to insert: " + data['id'])
        raise Exception(error) from None

if __name__ == "__main__":
    logging.info("Starting reddit_worker")
    try:
        w = Worker(['url_submit'], connection=redis_conn, log_job_description=False)
        w.work(logging_level=logging.WARNING)
    except Exception as error:
        logging.error(traceback.format_exc())
        logging.error(error)