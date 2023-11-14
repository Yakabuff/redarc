import json
import os
import falcon
from psycopg2.extras import RealDictCursor
import logging
logger = logging.getLogger('redarc')

class Unlist:
   def __init__(self, pool):
      self.pool = pool

   def on_post(self, req, resp):
      obj = req.get_media()
      subreddit = obj.get('subreddit')
      unlist = obj.get('unlist')
      pw = obj.get('password')

      if pw != os.getenv('ADMIN_PASSWORD'):
         resp.status = falcon.HTTP_401
         return
      
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute('UPDATE subreddits SET unlisted = %s WHERE name = %s', [unlist, subreddit])
         pg_con.commit()
      except Exception as error:
         logger.error(error)
         resp.status = falcon.HTTP_500
         return
      finally:
         self.pool.putconn(pg_con)

      resp.status = falcon.HTTP_200
