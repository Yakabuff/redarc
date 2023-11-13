from logging.handlers import RotatingFileHandler
import os
import sys
import time
import traceback
from dotenv import load_dotenv
import logging
from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values
from psycopg2 import pool
import psycopg2

load_dotenv()
if not os.path.exists('logs'):
   os.makedirs('logs')
filename = 'logs/index_worker.log'
handler = RotatingFileHandler(filename,
                           maxBytes=1024*1024*10,
                           backupCount=10)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                     encoding='utf-8',
                     level=logging.INFO,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     handlers=[handler])
try:
   pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                         password=os.getenv('PG_PASSWORD'),
                                                         host=os.getenv('PG_HOST'),
                                                         port=os.getenv('PG_PORT'),
                                                         database=os.getenv('PG_DATABASE'))

   pg_pool_fts = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PGFTS_USER'),
                                                         password=os.getenv('PGFTS_PASSWORD'),
                                                         host=os.getenv('PGFTS_HOST'),
                                                         port=os.getenv('PGFTS_PORT'),
                                                         database=os.getenv('PGFTS_DATABASE'))

   pg_con = pg_pool.getconn()
   cursor = pg_con.cursor()
except Exception as error:
    logging.error(error)
    sys.exit(1)

last_submission_id = None
last_comment_id = None

def insert_search_submission(data):
   try:
      pgfts_con = pg_pool_fts.getconn()
      cursor = pgfts_con.cursor()

      insert_submission = """
      insert into submissions (id, subreddit, title, num_comments,
      score, gilded, created_utc, self_text)
      values %s ON CONFLICT (id) DO NOTHING
      """
      _data = []
      for i in data:
         _data.append(i[:-1]) # Remove retrieved_utc column
      # Bulk insert rows
      execute_values(cursor, insert_submission, _data)
      logging.info(f'Indexed {cursor.rowcount} submissions')
      
      pgfts_con.commit()
      pg_pool_fts.putconn(pgfts_con)
   except Exception as error:
      logging.error(error)
      logging.error(traceback.format_exc())
      raise Exception(error) from None

def insert_search_comment(data):
   try:
      pgfts_con = pg_pool_fts.getconn()
      cursor = pgfts_con.cursor()

      insert_comment = """
      insert into comments (id, subreddit, body, score, gilded,
      created_utc, link_id) values %s
      ON CONFLICT (id) DO NOTHING
      """
      _data = []
      for i in data:
         _data.append(i[:-1]) # Remove retrieved_utc column
      # Bulk insert rows
      execute_values(cursor, insert_comment, _data)
      logging.info(f'Indexed {cursor.rowcount} comments')
      
      pgfts_con.commit()
      pg_pool_fts.putconn(pgfts_con)
   except Exception as error:
      logging.error(error)
      logging.error(traceback.format_exc())
      raise Exception(error) from None

def update_search_indexed_status(_type, last_indexed):
   # Update status with most recently indexed posts
   table_type = "search_status_comments" if _type == "comments" else "search_status_submissions"
   update_sql = """
   update %s
   set
      created_utc = %s, retrieved_utc = %s;
   """
   insert_sql = """
   insert into %s (created_utc, retrieved_utc) values (%s, %s)
   """

   drop_sql = "delete from %s"

   if _type == 'comments':
      created_utc = last_indexed[5]
      retrieved_utc = last_indexed[-1]
   else:
      created_utc = last_indexed[6]
      retrieved_utc = last_indexed[-1]

   try:
      cursor.execute(update_sql, (AsIs(table_type), created_utc, retrieved_utc))
      if cursor.rowcount != 1:
         cursor.execute(drop_sql, (AsIs(table_type),))
         cursor.execute(insert_sql, (AsIs(table_type), created_utc, retrieved_utc)) #created_utc and retrieved_utc
      pg_con.commit()
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None

def index_db():
   # Update subreddits table with num posts, threads and new subreddits
   try:
      cursor.execute("select DISTINCT subreddit from submissions;")
      subreddits = cursor.fetchall()
      for row in subreddits:
         logging.debug("Updating index table:" + str(row[0]))
         cursor.execute("select COUNT(*) from submissions where subreddit = %s;", (row))
         num_submissions = cursor.fetchone()

         cursor.execute("select COUNT(*) from comments where subreddit = %s;", (row))
         num_comments = cursor.fetchone()

         cursor.execute("""INSERT INTO subreddits (name, unlisted, num_submissions, num_comments)
            VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET(num_submissions, num_comments) = (%s, %s)""",
            (row, False, num_submissions, num_comments, num_submissions, num_comments))
      pg_con.commit()

   except Exception as error:
      logging.error(error)

def find_submissions():
   try:
      cursor.execute('''select * from search_status_submissions''')
      sss = cursor.fetchone()
      if sss == None:
         sss = (0, 0) # (created_utc, retrieved_utc)
      cursor.execute('''select id, subreddit, title, num_comments,
                     score, gilded, created_utc, self_text,
                     retrieved_utc from submissions where retrieved_utc >= %s
                     ORDER BY retrieved_utc ASC, created_utc ASC 
                     LIMIT 10000''', (sss[1],))
      subs = cursor.fetchall()
      return subs
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None

def find_comments():
   try:
      cursor.execute('''select * from search_status_comments''')
      ssc = cursor.fetchone()
      if ssc == None:
         ssc = (0, 0)
      cursor.execute('''select id, subreddit, body, score, gilded, created_utc,
                     link_id, retrieved_utc from comments where retrieved_utc >= %s
                     ORDER BY retrieved_utc ASC, created_utc ASC  
                     LIMIT 10000''', (ssc[1],))
      coms = cursor.fetchall()
      return coms
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None  

def find_submissions_in_range():
   try:
      cursor.execute('''select * from search_status_submissions''')
      sss = cursor.fetchone()
      if sss == None:
         sss = (0, 0) # (created_utc, retrieved_utc)
      cursor.execute('''select id, subreddit, title, num_comments,
                     score, gilded, created_utc, self_text,
                     retrieved_utc from submissions where retrieved_utc = %s
                     and created_utc >= %s
                     ORDER BY retrieved_utc ASC, created_utc ASC 
                     LIMIT 10000''', (sss[1],sss[0]))
      subs = cursor.fetchall()
      return subs
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None

def find_comments_in_range():
   try:
      cursor.execute('''select * from search_status_comments''')
      ssc = cursor.fetchone()
      if ssc == None:
         ssc = (0, 0)
      cursor.execute('''select id, subreddit, body, score, gilded, created_utc,
                     link_id, retrieved_utc from comments where retrieved_utc = %s
                     and created_utc >= %s
                     ORDER BY retrieved_utc ASC, created_utc ASC  
                     LIMIT 10000''', (ssc[1],ssc[0]))
      coms = cursor.fetchall()
      return coms
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None  

def index_submissions():
   try:
      subs = find_submissions()
      if len(subs) > 0:
         insert_search_submission(subs)
         update_search_indexed_status('submissions', subs[-1])
      global last_submission_id

      # Check if indexer is processing new ids
      if subs[-1][0] == last_submission_id:
         # Check number of ids where retrieved_utc = %s > 10000 to really make sure no new submissions
         # If there are new submissions, find submissions again with created_utc and same retrieved_utc
         # and update index
         logging.info(f"No new submissions found in retrieved_utc date range {subs[-1][-1]}...")
         res = find_submissions_in_range()
         if len(res) > 0 and res[-1][0] != last_submission_id:
            logging.info(f"Found new submissions in retrieved_utc range: {res[-1][-1]} created_utc: {res[-1][5]}")
            insert_search_submission(res)
            update_search_indexed_status('submissions', res[-1])
            last_submission_id = res[-1][0]
            return True
         return False
      
      last_submission_id = subs[-1][0]
      return True
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None
   
def index_comments():
   try:
      coms = find_comments()
      if len(coms) > 0:
         insert_search_comment(coms)
         update_search_indexed_status('comments', coms[-1])
      global last_comment_id
      if coms[-1][0] == last_comment_id:
         logging.info(f"No new comments found in retrieved_utc date range {coms[-1][-1]}...")
         res = find_comments_in_range()
         if len(res) > 0 and res[-1][0] != last_comment_id:
            logging.info(f"Found new comments in retrieved_utc range: {res[-1][-1]} created_utc: {res[-1][5]}")
            insert_search_comment(res)
            update_search_indexed_status('comments', res[-1])
            last_comment_id = res[-1][0]
            return True
         return False
      last_comment_id = coms[-1][0]
      return True
   except Exception as error:
      logging.error(traceback.format_exc())
      raise Exception(error) from None

if __name__ == "__main__":
   logging.info("Starting index_worker")
   try:
      index_db()
      while True:
         res1 = index_submissions()
         res2 = index_comments()
         if ((res1 and res2) == False):
            logging.debug("No new threads/comments found... Sleeping")
            time.sleep(int(os.getenv('INDEX_DELAY')))
         else:
            index_db()
   except Exception as error:
      logging.error(error)
      logging.error(traceback.format_exc())

