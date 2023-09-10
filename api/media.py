import mimetypes
import os
import falcon
import logging
logger = logging.getLogger('redarc')

class Media:
   def __init__(self, path):
      self.base_path = path
      
   def on_get(self, req, resp):
      file = req.get_param('file', required=True)
      subreddit = req.get_param('subreddit', required=True)
      path = os.path.join(self.base_path, subreddit, file)
      try:
         content_length = os.path.getsize(path)
         resp.stream = open(path, 'rb')
      except Exception as error:
         logger.error(error)
         resp.status = falcon.HTTP_404 
         return
      resp.content_type = mimetypes.guess_type(path)[0]
      resp.status = falcon.HTTP_200 
      resp.content_length = content_length