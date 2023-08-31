import datetime
import os
import sys
import time
from dotenv import load_dotenv
import logging
from psycopg2.extensions import AsIs
from psycopg2 import pool
import psycopg2

load_dotenv()
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

def insert_search(_type, data):
   #Insert data into postgres fts
   try:
      pgfts_con = pg_pool_fts.getconn()
      cursor = pgfts_con.cursor()

      insert_submission = """
      insert into submissions (id, subreddit, title, num_comments, score, gilded, created_utc, self_text) values (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
      """

      insert_comment = """
      insert into comments (id, subreddit, body, score, gilded, created_utc, link_id) values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
      """
      for i in data:
         if _type == 'comments':
            cursor.execute(insert_comment, i[:-1])
         else:
            cursor.execute(insert_submission, i[:-1])
      pgfts_con.commit()
      pg_pool_fts.putconn(pgfts_con)
   except Exception as error:
      raise Exception(error) from None

# find n ids starting with lowest retrieved_utc and index_utc == None
def find_ids():
   # fetch search index progress for submissions/comments
   # fetch 10k submissions/comments sort by retrieved_utc and create_utc 
   # where retrieved_utc >= progress_retrieved_utc and created_utc >= progress_created_utc
   # Note: edge case where content previously indexed in same date range is indexed again
   try:
      cursor.execute('''select * from search_status_submissions''')
      sss = cursor.fetchone()
      if sss == None:
         sss = (0, 0)
      cursor.execute('''select id, subreddit, title, num_comments, score, gilded, created_utc, self_text, retrieved_utc from submissions where retrieved_utc >= %s
         and created_utc >= %s ORDER BY retrieved_utc ASC, created_utc ASC LIMIT 10000''', (sss[1], sss[0]))
      subs = cursor.fetchall()
      subs_indexed = len(subs)
      if len(subs) > 0:
         insert_search('submissions', subs)
         update_search_indexed_status('submissions', subs[-1])
      cursor.execute('''select * from search_status_comments''')
      ssc = cursor.fetchone()
      if ssc == None:
         ssc = (0, 0)
      cursor.execute('''select id, subreddit, body, score, gilded, created_utc, link_id, retrieved_utc from comments where retrieved_utc >= %s
         and created_utc >= %s ORDER BY retrieved_utc, created_utc ASC LIMIT 10000''', (ssc[1], ssc[0]))
      coms = cursor.fetchall()
      coms_indexed = len(coms)
      if len(coms) > 0:
         insert_search('comments', coms)
         update_search_indexed_status('comments', coms[-1])
      pg_con.commit()
      # pg_pool.putconn(pg_con)
      return (subs_indexed, coms_indexed)
   except Exception as error:
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
   except Exception as error:
      raise Exception(error) from None

def index_db():
   # Update subreddits table with num posts, threads and new subreddits
   try:
      cursor.execute("select DISTINCT subreddit from submissions;")
      subreddits = cursor.fetchall()
      cursor.execute("DELETE from subreddits;")
      for row in subreddits:
         logging.info("Updating index table:" + str(row[0]))
         cursor.execute("select COUNT(*) from submissions where subreddit = %s;", (row))
         num_submissions = cursor.fetchone()

         cursor.execute("select COUNT(*) from comments where subreddit = %s;", (row))
         num_comments = cursor.fetchone()

         cursor.execute("""INSERT INTO subreddits (name, unlisted, num_submissions, num_comments)
            VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET(num_submissions, num_comments) = (%s, %s)""",
            (row, False, num_submissions, num_comments, num_submissions, num_comments))
      pg_con.commit()
      # pg_con.close()
   except Exception as error:
      logging.error(error)

if __name__ == "__main__":
   time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
   if not os.path.exists('logs'):
      os.makedirs('logs')
   logging.basicConfig(filename='logs/index_worker-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)
   try:
      index_db()
      while True:
         res = find_ids()
         if (res[0] < 10000 and res[1] < 10000):
            index_db()
            time.sleep(int(os.getenv('INDEX_DELAY')))
   except Exception as error:
      logging.error(error)

