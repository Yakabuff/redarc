import calendar
import datetime
import json
import os
import time
from psycopg2.extras import execute_values
from worker.con import pg_pool
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from dotenv import load_dotenv
import logging

load_dotenv()

es_client = Elasticsearch(os.getenv('ES_HOST'), basic_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')))
pg_con = pg_pool.getconn()
cursor = pg_con.cursor()
# every x minutes iterate through every file.
# if > 50 mb, index and delete file
# if time delta > x minutes, index and delete file
def bulk_insert(_type, data):
   actions = []

   for i in data:
      id = i[0]

      if _type == 'comments':
         dt_utc = i[6].replace(tzinfo=datetime.timezone.utc)
         unixtime = int(calendar.timegm(dt_utc.utctimetuple())) 
         meta = json.dumps(
            {
               'create': {
                  '_index':'redarc_comments_tmp',
                  "_id": id,
               },
            }
         )
         data = json.dumps(
            {
               'body': i[2],
               'score': i[8],
               'created_utc': unixtime,
               'type': "comment",
               'subreddit': i[1],
               'link_id': i[8]
            }
         )
      else:
         dt_utc = i[10].replace(tzinfo=datetime.timezone.utc)
         unixtime = int(calendar.timegm(dt_utc.utctimetuple())) 
         meta = json.dumps(
            {
               'create': {
                  '_index':'redarc_tmp',
                  "_id": id,
               },
            }
         )
         data = json.dumps(
            {
               'title': i[2],
               'self_text': i[11],
               'score': i[8],
               'created_utc': unixtime,
               'type': "submission",
               'subreddit': i[1]
            }
         )
      actions.append(meta)
      actions.append(data)

   return es_client.bulk(operations=actions, index='redarc_tmp')

# find n ids starting with lowest retrieved_utc and index_utc == None
def find_ids():

   cursor.execute('select id from status_submissions where visible = true and retrieved_utc is not NULL and indexed_utc is NULL ORDER BY retrieved_utc ASC LIMIT 10000')
   ids = sum(tuple(cursor.fetchall()), ())

   cursor.execute('select * from submissions where id in %s', (ids,))
   subs = cursor.fetchall()
   res = bulk_insert('submissions', subs)
   update_indexed_status("subsmissions", res)

   cursor.execute('select id from status_comments where visible = true and retrieved_utc is not NULL and indexed_utc is NULL ORDER BY retrieved_utc ASC LIMIT 10000')
   ids = sum(tuple(cursor.fetchall()), ())
   cursor.execute('select * from comments where id in %s', (ids,))
   coms = cursor.fetchall()
   res = bulk_insert('comments', coms)
   update_indexed_status("comments", res)
   pg_con.commit()
   pg_pool.putconn(pg_con)

def update_indexed_status(_type, res):
   _type = "status_comments" if _type == "comments" else "status_submissions"
   _time = int(time.time())
   sql = """
   update status_submissions
   set
      indexed_utc = t.time
   from (values %s) as t(id, time)
   where status_submissions.id = t.id;
   """
   print(sql)
   rows_to_update = []
   for i in res['items']:
      if 'error' in i['create']:
         logging.error('Failed to index ' + str(i['create']['_id']))
         logging.error(i['create']['error'])
      else:
         logging.info('Indexed ' + str(i['create']['_id']))
         logging.info(i['create']['status'])
         rows_to_update.append((i['create']['_id'], _time))
   print(rows_to_update)
   execute_values(cursor, sql, rows_to_update)

if __name__ == "__main__":
   time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
   logging.basicConfig(filename='es_worker-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)
   while True:
      find_ids()
      time.sleep(3600)

