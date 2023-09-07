import json
import falcon
from psycopg2.extras import RealDictCursor
import logging
logger = logging.getLogger('redarc')

class Status:
   def __init__(self, pool):
      self.pool = pool

   def on_get(self, req, resp):
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute('SELECT job_id, start_utc, finish_utc, error FROM progress WHERE job_id = %s', [req.get_param('job_id')])
         status = cursor.fetchone()
      except Exception as error:
         logger.error(error)
         resp.status = falcon.HTTP_500
         return
      finally:
         self.pool.putconn(pg_con)

      resp.text= json.dumps([status])
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200
