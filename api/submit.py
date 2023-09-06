import json
import re
import falcon
import os
import logging
import hashlib
from rq.job import JobStatus

logger = logging.getLogger('redarc')

class Submit:
    def __init__(self, url_queue):
      self.url_queue = url_queue

    def on_post(self, req, resp):

      if os.getenv('INGEST_ENABLED') == 'false':
        resp.text = json.dumps({"status": "ingest disabled", "url": ""})
        resp.status = falcon.HTTP_501
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
      
      id = hashlib.md5(id.encode('utf-8')).hexdigest() 
      exists = self.job_exists(id)
      if exists[0] == True:
        resp.text = json.dumps({"status": "success", "id": id, "position": exists[1].get_position()}, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return

      try:
        job = self.url_queue.enqueue('worker.reddit_worker.fetch_thread', thread_id=id, url=url, job_id=id)
        if job.get_status(refresh=True) == "queued":
          resp.text = json.dumps({"status": "success", "id": id, "position": job.get_position()}, ensure_ascii=False)
          resp.status = falcon.HTTP_200
        else:
          logger.error(f"Failed to enqueue job: thread ID {id}")
          resp.text = json.dumps({"status": "failed", "id": id}, ensure_ascii=False)
          resp.status = falcon.HTTP_500
      except Exception as error:
        logger.error(f"Failed to enqueue job: thread ID {id}")
        logger.error(error)
        resp.status = falcon.HTTP_500
        resp.text = json.dumps({"status": "failed"}, ensure_ascii=False)

    def job_exists(self, id):
      job = self.url_queue.fetch_job(id)  
      if job == None:
        return (False, None)   
      status = job.get_status()
      if status in {JobStatus.QUEUED, JobStatus.SCHEDULED}:
        # Job exists and will be run.
        return (True, job)
      return (False, None)