import json
import falcon
from psycopg2.extras import RealDictCursor

class Comments:
   def __init__(self, pool):
      self.pool = pool

   def on_get(self, req, resp):
      text = 'SELECT * FROM comments where'
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

      if req.get_param('parent_id'):
         if len(params) != 0:
            text += ' and'

         params.append(req.get_param('parent_id'))
         text += ' parent_id = %s'   

      if req.get_param('link_id'):
         if len(params) != 0:
            text += ' and'

         params.append(req.get_param('link_id'))
         text += ' link_id = %s'  

      if req.get_param('sort') == 'ASC':
         text += ' ORDER BY created_utc ASC'
      else:
         text += ' ORDER BY created_utc DESC'

      if not req.get_param('parent_id') and not req.get_param('link_id'):
         text += ' LIMIT 500'

      if len(params) == 0:
         resp.status = falcon.HTTP_500
         return

      try:
         pg_con = self.pool.getconn()
         cursor = pg_con.cursor(cursor_factory=RealDictCursor)
         cursor.execute(text, params)
         comments = cursor.fetchall()
      except Exception as error:
         resp.status = falcon.HTTP_500
         return
      if req.get_param_as_bool('unflatten') == True and req.get_param('link_id'):
         resp.text = json.dumps(unflatten(comments, req.get_param('link_id')))
         resp.content_type = falcon.MEDIA_JSON
         resp.status = falcon.HTTP_200
         return
      
      resp.text= json.dumps(list(comments))
      resp.content_type = falcon.MEDIA_JSON
      resp.status = falcon.HTTP_200

def unflatten(data, root):
   """
   Turn array of comments into hashmap. Add empty array field replies to comment obj
	Iterate over keys
	If comment's parent is root, push to commentTree list. These are top level comments
	find parent comment in hashmap and append this comment into parent's reply. 
	Set replies of root to commentTree 
   """

   lookup = array_to_lookup(data)
   comment_tree = []

   for id in lookup:
      comment = lookup[id]
      parent_id = comment.parent_id
      if parent_id == root:
         comment_tree.append(comment)
      else:
         if lookup[parent_id] == None:
            comment_tree.append(Comment({'body': "[comment not found]", 'author': "[unknown]", 'id': id, 'replies': [comment], 'parent_id': root, 'link_id': root}))
   # print(comment_tree)
   return comment_tree

def array_to_lookup(data):
   """
   Turn array of comments into a hashmap id -> comment
   """
   lookup = {}
   for comment in data:
      c = Comment(comment)
      lookup[comment['id']] = c

   for i in lookup:
      pid = lookup[i].parent_id
      if pid in lookup:
         lookup[pid].replies.append(lookup[i])

   return lookup


class Comment(dict):
   def __init__(self, comment):
      super().__init__()
      self.__dict__ = self
      self.id = comment['id']
      self.author = comment['author']
      self.body = comment['body']
      self.parent_id = comment['parent_id']
      self.link_id = comment['link_id']
      self.subreddit = comment['subreddit']
      self.created_utc = comment['created_utc']
      self.score = comment['score']
      self.gilded = comment['gilded']
      self.replies = []