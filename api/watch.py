import json
import os
import falcon
from psycopg2.extras import RealDictCursor
import logging
logger = logging.getLogger('redarc')

class Watch:
   def __init__(self, pool):
      self.pool = pool

   def on_post(self, req, resp):
      obj = req.get_media()
      subreddit = obj.get('subreddit')
      action = obj.get('action')
      pw = obj.get('password')

      if pw != os.getenv('ADMIN_PASSWORD'):
         resp.status = falcon.HTTP_401
         return
      
      if action != "add" and action != "remove":
         resp.status = falcon.HTTP_500
         return
      
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         if action == "add":
            cursor.execute('INSERT INTO watch(name) VALUES(%s) ON CONFLICT (name) DO NOTHING', [subreddit])
         else:
            cursor.execute('DELETE FROM watch where name = %s', [subreddit])
         pg_con.commit()
      except Exception as error:
         logger.error(error)
         resp.status = falcon.HTTP_500
         return
      finally:
         self.pool.putconn(pg_con)

      resp.status = falcon.HTTP_200
