import datetime
import logging
from worker.validate import validate_submission, validate_comment
from worker.con import reddit
from worker.con import pg_pool
import time
from enum import Enum
import time
from rq import Worker
from redarc_ingest.conn import redis_conn
"""
Redarc worker

1) Make reddit request
2) Insert into DB if comment/submission ID does not exist.  If exist, update gilded, upvotes if number higher.  Update score
"""

class type(Enum):
    SUBMISSION = 1
    COMMENT = 2

def fetch_thread(thread_id):
    logging.info("Fetching submission "+ str(thread_id))
    submission = reddit.submission(id=thread_id)
    process_submission(submission)
    comments = submission.comments
    comments.replace_more(limit=None)
    for comment in comments.list():
        process_comment(comment)

def process_submission(submission):
    x = validate_submission(submission)
    logging.info("Processing submission: " + x['id'])
    if x != None:
        insert_db(type.SUBMISSION, x)
        # queue_index(type.SUBMISSION, x)


def process_comment(comment):
    x = validate_comment(comment)
    logging.info("Processing comments: " + x['id'])
    if x != None:
        insert_db(type.COMMENT, x)
        # queue_index(type.COMMENT, x)

def insert_db(_type, data):
    try:
        pg_con = pg_pool.getconn()
        # Update score, get max of gilded, get max of num_comments
        cursor = pg_con.cursor()
        if _type == type.SUBMISSION:
            cursor.execute('INSERT INTO submissions(id, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING',
                            [data['id'], data['subreddit'], data['title'], data['author'], data['permalink'], data['thumbnail'], data['num_comments'], data['url'], data['score'], data['gilded'], data['created_utc'], data['selftext'], data['is_self']])
            cursor.execute('UPDATE submissions SET num_comments=GREATEST(num_comments, %s), gilded=GREATEST(gilded, %s), score=%s where id =%s', [data['num_comments'], data['gilded'], data['score'], data['id']])
            cursor.execute('INSERT INTO status_submissions(id, visible, retrieved_utc, indexed_utc) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [data['id'], True, int(time.time()), None])
        else:
            cursor.execute('INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id) VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING',
                            [data['id'], data['subreddit'], data['body'], data['author'], data['score'], data['gilded'], data['created_utc'], data['parent_id'], data['link_id']])
            cursor.execute('UPDATE comments SET gilded=GREATEST(gilded, %s), score=%s where id =%s',
                            [data['gilded'], data['score'], data['id']])
            cursor.execute('INSERT INTO status_comments(id, visible, retrieved_utc, indexed_utc) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [data['id'], True, int(time.time()), None])
        
        pg_con.commit()
        pg_pool.putconn(pg_con)
    except Exception as error:
        logging.error("Failed to insert: " + data['id'])
        logging.error(error)

if __name__ == "__main__":
    time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
    logging.basicConfig(filename='reddit_worker-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)
    w = Worker(['url_submit'], connection=redis_conn)
    w.work()