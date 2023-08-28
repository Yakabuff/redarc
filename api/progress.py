import json
import falcon
import os
from psycopg2.extras import RealDictCursor

class Progress:
   def __init__(self, pool):
      self.pool = pool

   def on_post(self, req, resp):
      obj = req.get_media()
      if obj.get('password') != os.getenv('ADMIN_PASSWORD'):
         resp.status = falcon.HTTP_401
         return
      
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute('SELECT * FROM progress ORDER BY start_utc DESC LIMIT 200')
         progress = cursor.fetchall()
      except Exception as error:
         print(error)
         resp.status = falcon.HTTP_500
         return
      
      resp.text= json.dumps(list(progress))
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200
