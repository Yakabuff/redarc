import json
import falcon
from psycopg2.extras import RealDictCursor

class Subreddits:
   def __init__(self, pool):
      self.pool = pool

   def on_get(self, req, resp):
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute('select * from subreddits')
         subs = cursor.fetchall()
      except Exception as error:
         resp.status = falcon.HTTP_500
         return
      
      s = filter(lambda x: (x['unlisted'] == False), subs)
      out = json.dumps(list(s))
      resp.text= out
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200
