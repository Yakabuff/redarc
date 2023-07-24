def validate_submission(submission):
   if submission.id and isinstance(submission.id, str):
      identifier = submission.id.strip().replace("\u0000", "").lower()
   elif submission.name and isinstance(submission.name, str) and len(submission.name.split('_')) > 1:
      identifier = submission.name.strip().replace("\u0000", "").lower()
      identifier = identifier.split('_')[1]
   else:
      return None

   if submission.subreddit.display_name and isinstance(submission.subreddit.display_name, str):
      subreddit = submission.subreddit.display_name.strip().replace("\u0000", "").lower()
   else:
      return None

   if submission.title and isinstance(submission.title, str):
      title = submission.title.strip().replace("\u0000", "")
   else:
      title = ""

   if submission.author.name and isinstance(submission.author.name, str):
      author = submission.author.name.strip().replace("\u0000", "").lower()
   else:
      author = "[unknown]"

   if submission.permalink and isinstance(submission.permalink, str):
      permalink = submission.permalink.strip().replace("\u0000", "")
   else:
      permalink = f'/r/{subreddit}/comments/{identifier}/foobar'

   if submission.num_comments and isinstance(submission.num_comments, int):
      num_comments = submission.num_comments
   elif submission.num_comments and isinstance(submission.num_comments, str) and submission.num_comments.isdigits():
      num_comments = int(submission.num_comments)
   else:
      num_comments = 0

   if submission.url and isinstance(submission.url, str):
      url = submission.url.strip().replace("\u0000", "")
   else:
      url = f'http://reddit.com/r/{subreddit}/comments/{identifier}/blah'

   if submission.score and isinstance(submission.score, int):
      score = submission.score
   elif submission.score and isinstance(submission.score, str) and submission.score.isdigits():
      score = int(submission.score)
   else:
      score = 0

   if submission.gilded and isinstance(submission.gilded, int):
      gilded = submission.gilded
   elif submission.gilded and isinstance(submission.gilded, str) and submission.gilded.isdigits():
      gilded = int(submission.gilded)
   else:
      gilded = 0

   if submission.created_utc and isinstance(submission.created_utc, (int, float, complex)):
      created_utc = int(submission.created_utc)
   elif submission.created_utc and isinstance(submission.created_utc, str) and submission.created_utc.isdigit():
      created_utc = int(submission.created_utc)
   else:
      created_utc = 0

   if submission.selftext and isinstance(submission.selftext, str):
      selftext = submission.selftext.strip().replace("\u0000", "")
   else:
      selftext = ""

   if submission.is_self and isinstance(submission.is_self, bool):
      is_self = submission.is_self
   else:
      # Guess if self post
      is_self = True if "reddit.com/r/" in url else False

   if submission.thumbnail and isinstance(submission.thumbnail, str):
      thumbnail = submission.thumbnail.strip().replace("\u0000", "")
   else:
      if is_self:
         thumbnail = "self"
      else:
         thumbnail = "default"

   return {
        "title": title,
        "id": identifier,
        "author": author,
        "subreddit": subreddit,
        "created_utc": created_utc,
        "is_self": is_self,
        "permalink": permalink,
        "selftext": selftext,
        "num_comments": num_comments,
        "url": url,
        "permalink": permalink,
        "thumbnail": thumbnail,
        "score": score,
        "gilded": gilded,
    }

def validate_comment(comment):
   if comment.id and isinstance(comment.id, str):
      identifier = comment.id.strip()
   else:
      return None

   if comment.subreddit.display_name and isinstance(comment.subreddit.display_name, str):
      subreddit = comment.subreddit.display_name.strip().lower()
   else:
      return None
   if comment.author and isinstance(comment.author.name, str):
      author = comment.author.name.strip().lower()
   else:
      author = "[unknown]"
   
   if comment.score and isinstance(comment.score, int):
      score = comment.score
   elif comment.score and isinstance(comment.score, str) and comment.score.isdigits():
      score = int(comment.score)
   else:
      score = 0
   
   if comment.gilded and isinstance(comment.gilded, int):
      gilded = comment.gilded
   elif comment.gilded and isinstance(comment.gilded, str) and comment.gilded.isdigits():
      gilded = int(comment.gilded)
   else:
      gilded = 0

   if comment.created_utc and isinstance(comment.created_utc, (int, float, complex)):
      created_utc = int(comment.created_utc)
   elif comment.created_utc and isinstance(comment.created_utc, str) and comment.created_utc.isdigit():
      created_utc = int(comment.created_utc)
   else:
      created_utc = 0

   if comment.body and isinstance(comment.body, str):
      # delete null chars
      body = comment.body.strip().replace("\u0000", "")
   else:
      body = ""

   if comment.link_id and isinstance(comment.link_id, str):
      if len(comment.link_id.split('_')) > 1:
         link_id = comment.link_id.strip().split('_')[1]
      else:
         link_id = comment.link_id.strip()
   else:
      return None

   if comment.parent_id and isinstance(comment.parent_id, str):
      if len(comment.parent_id.split('_')) > 1:
         parent_id = comment.parent_id.strip().split('_')[1]
      else:
         parent_id = comment.parent_id.strip()
   else:
      parent_id = link_id

   return {
      'id': identifier,
      'subreddit': subreddit,
      'body': body,
      'author': author,
      'score': score,
      'gilded': gilded,
      'created_utc': created_utc,
      'parent_id': parent_id,
      'link_id': link_id
   }