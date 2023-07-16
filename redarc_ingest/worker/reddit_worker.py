import glob
import json
import os
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
3) Insert into DB if comment/submission ID does not exist.  If exist, update num_comments based on data from db.  Update gilded, upvotes if number higher
4) Store data in files
5) Flush data to elasticsearch if file > 50mb or time > x minutes
"""

class type(Enum):
    SUBMISSION = 1
    COMMENT = 2

def fetch_thread(thread_id):
    print("Fetching submission..")
    submission = reddit.submission(id=thread_id)
    process_submission(submission)
    comments = submission.comments
    comments.replace_more(limit=None)
    for comment in comments.list():
        process_comment(comment)

def process_submission(submission):
    print("processing submission")
    x = validate_submission(submission)
    if x != None:
        insert_db(type.SUBMISSION, x)
        # queue_index(type.SUBMISSION, x)


def process_comment(comment):
    print("processing comments")
    x = validate_comment(comment)
    print(x)
    if x != None:
        insert_db(type.COMMENT, x)
        # queue_index(type.COMMENT, x)

def insert_db(_type, data):
    pg_con = pg_pool.getconn()
    # Update score, get max of gilded, re-fetch num_comments
    cursor = pg_con.cursor()
    if _type == type.SUBMISSION:
        # x = cursor.execute("select num_comments from submissions where id = %s", [data.identifier])
        cursor.execute('INSERT INTO submissions(id, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING',
                        [data['id'], data['subreddit'], data['title'], data['author'], data['permalink'], data['thumbnail'], data['num_comments'], data['url'], data['score'], data['gilded'], data['created_utc'], data['selftext'], data['is_self']])
        # cursor.execute('UPDATE submissions SET num_comments=%s, gilded=GREATEST(gilded, %s), score=%s where id =%s', [x+1, data.gilded, data.score, data.identifier])
        cursor.execute('INSERT INTO status_submissions(id, visible, retrieved_utc, indexed_utc) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [data['id'], True, int(time.time()), None])
    else:
        cursor.execute('INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id) VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING',
                        [data['id'], data['subreddit'], data['body'], data['author'], data['score'], data['gilded'], data['created_utc'], data['parent_id'], data['link_id']])
        cursor.execute('INSERT INTO status_comments(id, visible, retrieved_utc, indexed_utc) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [data['id'], True, int(time.time()), None])
        # cursor.execute('UPDATE comments SET gilded=GREATEST(gilded, %s), score=%s where id =%s',
        #                 [data.gilded, data.score, data.identifier])
    
    pg_con.commit()
    pg_pool.putconn(pg_con)

if __name__ == "__main__":
    w = Worker(['url_submit'], connection=redis_conn)
    w.work()