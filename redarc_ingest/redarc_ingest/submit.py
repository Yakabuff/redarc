import json
import re
from .conn import url_queue
import falcon
from worker.reddit_worker import fetch_thread
import os

class Submit:

    def on_post(self, req, resp):

      if os.getenv('INGEST_ENABLED') == 'false':
        resp.text = json.dumps({"status": "ingest disabled", "url": url}, ensure_ascii=False)
        resp.status = falcon.HTTP_500
        return        
      obj = req.get_media()
      url = obj.get('url')
      pw = obj.get('password')

      if os.getenv('INGEST_PASSWORD'):
        if pw != os.getenv('INGEST_PASSWORD'):
          resp.status = falcon.HTTP_401
          return

      if 'redd.it' in url:
        if re.search(r'\S+redd\.it\/\S+\/?$', url) == None:
          resp.text = json.dumps({"status": "invalid url", "url": url}, ensure_ascii=False)
          resp.status = falcon.HTTP_500
          return
        else:
          x = url.split('/')
          for i in x:
            if 'redd.it' in i:
              id = x[x.index(i) + 1]
      elif 'reddit.com/r/' in url:
        if re.search(r'\S+reddit\.com\/r\/\S+\/comments\/\S+\/\S+\/?$', url) == None:
          resp.text = json.dumps({"status": "invalid url", "url": url}, ensure_ascii=False)
          resp.status = falcon.HTTP_500
          return
        else:
          x = url.split('/')
          for i in x:
            if 'reddit.com' in i:
              id = x[x.index(i) + 4]
      else:
        resp.text = json.dumps({"status": "invalid url", "url": url}, ensure_ascii=False)
        resp.status = falcon.HTTP_500
        return
         
      job = url_queue.enqueue(fetch_thread, id)
      if job.get_status(refresh=True) == "queued":
        resp.text = json.dumps({"status": "success", "id": id, "position": job.get_position()}, ensure_ascii=False)
        resp.status = falcon.HTTP_200
      else:
        resp.text = json.dumps({"status": "failed", "id": id}, ensure_ascii=False)
        resp.status = falcon.HTTP_500