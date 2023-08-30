import json
import falcon
from psycopg2.extras import RealDictCursor
import logging
logger = logging.getLogger('redarc')

COMMENT = "comment"
SUBMISSION = "submission"

class Search:
   def __init__(self, pool):
      self.pool = pool

   def on_get(self, req, resp):
      type = ""
      self.type = req.get_param('type', required=True)
      if self.type != "submission" and self.type != "comment":
         resp.status = falcon.HTTP_500
         return
      
      self.subreddit= req.get_param('subreddit', required=True)
      self.search_phrase = req.get_param('search', required=True)   
      self.before = req.get_param('before') 
      if self.before != None and not self.before.isnumeric():
         resp.status = falcon.HTTP_500
         return
   
      self.after = req.get_param('after')
      if self.after != None and not self.after.isnumeric():
         resp.status = falcon.HTTP_500
         return
      
      self.search(resp)

   def search(self, resp):
      text = ''
      if self.type == SUBMISSION:
         text = 'SELECT * FROM submissions where'
      else:
         text = 'SELECT * FROM comments where'
      
      values = []

      values.append(self.subreddit.lower())
      text += ' subreddit = %s'
      
      if self.after:
         values.append(self.after)
         text += ' and created_utc > %s'
      
      if self.before:
         values.append(self.before)
         text += ' and created_utc < %s'
      
      values.append(self.search_phrase)
      text += ' and ts @@ phraseto_tsquery(%s)'

      # if req.get_param('sort') == 'asc':
      #    text += ' ORDER BY created_utc ASC'
      # else:
      #    text += ' ORDER BY created_utc DESC'
      text += ' ORDER BY created_utc DESC'
      text += ' LIMIT 100'
      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute(text, values)
         results = cursor.fetchall()
      except Exception as error:
         logger.error(error)
         resp.status = falcon.HTTP_500
         return
      resp.text= json.dumps(list(results))
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200