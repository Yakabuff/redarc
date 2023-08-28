import json
import falcon
from psycopg2.extras import RealDictCursor

class Submissions:
   def __init__(self, pool):
      self.pool = pool

   def on_get(self, req, resp):
      text = 'SELECT * FROM submissions where'
      params = []

      if req.get_param('id'):
         text += ' id = %s'
         params.append(req.get_param('id'))

      if req.get_param('subreddit'):
         if len(params) != 0:
            text += ' and'

         params.append(str(req.get_param('subreddit')).lower())
         text += ' subreddit = %s'

      if req.get_param_as_int('after'):
         if len(params) != 0:
            text += ' and'

         params.append(req.get_param_as_int('after'))
         text += ' created_utc > %s'

      if req.get_param_as_int('before'):
         if len(params) != 0:
            text += ' and'

         params.append(req.get_param_as_int('before'))
         text += ' created_utc < %s'      

      if req.get_param('sort') == 'ASC':
         text += ' ORDER BY created_utc ASC'
      else:
         text += ' ORDER BY created_utc DESC'

      text += ' LIMIT 100'

      if len(params) == 0:
         resp.status = falcon.HTTP_500
         return

      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute(text, params)
         submissions = cursor.fetchall()
      except Exception as error:
         resp.status = falcon.HTTP_500
         return
      
      resp.text= json.dumps(list(submissions))
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200
