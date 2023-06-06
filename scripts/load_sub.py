import json
import psycopg2
import sys
import logging
import datetime

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
logging.basicConfig(filename='submission-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)

filename = sys.argv[1]
conn = psycopg2.connect(
  database="postgres",
  user='postgres',
  password='test1234',
  host='localhost',
  port='5432'
)
line_number = 0
cursor = conn.cursor()

with open(filename) as file:
  for line in file:
      line_number = line_number + 1
      line = line.rstrip()
      sub_dict = json.loads(line)

      # id is occasionally missing.  Use the 'name' field to derive id
      if 'id' in sub_dict and isinstance(sub_dict['id'], str):
        identifier = sub_dict['id'].strip().replace("\u0000", "").lower()
      elif 'name' in sub_dict and isinstance(sub_dict['name'], str) and len(identifier.split('_')) > 1:
        identifier = sub_dict['name'].strip().replace("\u0000", "").lower()
        identifier = identifier.split('_')[1]
      else:
        logging.error("Could not find ID")
        logging.debug("Line number: "+ str(line_number))
        print("================================")
        continue

      if 'subreddit' in sub_dict and isinstance(sub_dict['subreddit'], str):
        subreddit = sub_dict['subreddit'].strip().replace("\u0000", "").lower()
      else:
        logging.error("Could not find subreddit for: " + identifier)
        logging.debug("Line number: "+ str(line_number))
        print("================================")
        continue

      if 'title' in sub_dict and isinstance(sub_dict['title'], str):
        title = sub_dict['title'].strip().replace("\u0000", "")
      else:
        logging.warning("Could not find title for: " + identifier)
        logging.debug("Line number: "+ str(line_number))
        title = ""

      if 'author' in sub_dict and isinstance(sub_dict['author'], str):
        author = sub_dict['author'].strip().replace("\u0000", "").lower()
      else:
        logging.warning("Could not find author in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        author = "[unknown]"

      if 'permalink' in sub_dict and isinstance(sub_dict['permalink'], str):
        permalink = sub_dict['permalink'].strip().replace("\u0000", "")
      else:
        logging.warning("Could not find permalink in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        permalink = f'/r/{subreddit}/comments/{identifier}/foobar'

      if 'num_comments' in sub_dict and isinstance(sub_dict['num_comments'], int):
        num_comments = sub_dict['num_comments']
      elif 'num_comments' in sub_dict and isinstance(sub_dict['num_comments'], str) and sub_dict['num_comments'].isdigits():
        num_comments = int(sub_dict['num_comments'])
      else:
        logging.warning("Could not find num_comments in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        num_comments = 0

      if 'url' in sub_dict and isinstance(sub_dict['url'], str):
        url = sub_dict['url'].strip().replace("\u0000", "")
      else:
        url = f'http://reddit.com/r/{subreddit}/comments/{identifier}/blah'
        logging.warning("Could not find url in " + identifier)
        logging.debug("Line number: "+ str(line_number))

      if 'score' in sub_dict and isinstance(sub_dict['score'], int):
        score = sub_dict['score']
      elif 'score' in sub_dict and isinstance(sub_dict['score'], str) and sub_dict['score'].isdigits():
        score = int(sub_dict['score'])
      else:
        logging.warning("Could not find score in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        score = 0

      if 'gilded' in sub_dict and isinstance(sub_dict['gilded'], int):
        gilded = sub_dict['gilded']
      elif 'gilded' in sub_dict and isinstance(sub_dict['gilded'], str) and sub_dict['gilded'].isdigits():
        gilded = int(sub_dict['gilded'])
      else:
        logging.warning("Could not find gilded in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        gilded = 0

      if 'created_utc' in sub_dict and isinstance(sub_dict['created_utc'], int):
        created_utc = sub_dict['created_utc']
      elif 'created_utc' in sub_dict and isinstance(sub_dict['created_utc'], str) and sub_dict['created_utc'].isdigit():
        created_utc = int(sub_dict['created_utc'])
      else:
        logging.error("Could not find created_utc in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        created_utc = 0

      if 'selftext' in sub_dict and isinstance(sub_dict['selftext'], str):
        self_text = sub_dict['selftext'].strip().replace("\u0000", "")
      else:
        logging.warning("Could not find selftext in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        self_text = ""

      if 'is_self' in sub_dict and isinstance(sub_dict['is_self'], bool):
        is_self = sub_dict['is_self']
      else:
        logging.warning("Could not find is_self in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        # Guess if self post
        is_self = True if "reddit.com/r/" in url else False

      if 'thumbnail' in sub_dict and isinstance(sub_dict['thumbnail'], str):
        thumbnail = sub_dict['thumbnail'].strip().replace("\u0000", "")
      else:
        logging.warning("Could not find thumbnail in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        if is_self:
          thumbnail = "self"
        else:
          thumbnail = "default"

      print('====================')
      try:
        cursor.execute('INSERT INTO submissions(id, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING', [identifier, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self])
      except Exception as error:
        logging.error("ERROR: "+ str(error))
        logging.debug("Line number: "+ str(line_number))
        logging.debug(identifier)
        logging.debug(subreddit)
        logging.debug(title)
        logging.debug(author)
        logging.debug(permalink)
        logging.debug(thumbnail)
        logging.debug(num_comments)
        logging.debug(url)
        logging.debug(score)
        logging.debug(gilded)
        logging.debug(created_utc)
        logging.debug(self_text)
        logging.debug(is_self)
        logging.debug("================================")
        continue
      print(f"Identifier inserted succesfully {identifier}")
conn.commit()
conn.close()
