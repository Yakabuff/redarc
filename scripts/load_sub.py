import json
import psycopg2
import sys
filename = sys.argv[1]
conn = psycopg2.connect(
  database="postgres",
  user='postgres',
  password='test1234',
  host='localhost',
  port='5432'
)
cursor = conn.cursor()
cursor.execute('BEGIN;')
with open(filename) as file:
  for line in file:
      line = line.rstrip()
      sub_dict = json.loads(line)
      # Rollback if id or subreddit not found.  Data is essentially useless
      # id is sometimes called name in dumps
      if 'id' in sub_dict and isinstance(sub_dict['id'], str):
        identifier = sub_dict['id'].strip()
      elif 'name' in sub_dict and isinstance(sub_dict['name'], str):
        identifier = sub_dict['name'].strip()
        identifier = identifier.split('_')[1]
      else:
        print("error: could not find ID")
        print("================================")
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)

      if 'subreddit' in sub_dict and isinstance(sub_dict['subreddit'], str):
        subreddit = sub_dict['subreddit'].strip()
      else:
        print("error: could not find subreddit for: " + identifier)
        print("================================")
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)

      if 'title' in sub_dict and isinstance(sub_dict['title'], str):
        title = sub_dict['title'].strip()      
      else:
        print("warning: could not find title for: " + identifier)
        title = ""

      if 'author' in sub_dict and isinstance(sub_dict['author'], str):
        author = sub_dict['author'].strip()
      else:
        print("warning: could not find author in " + identifier)
        author = "[unknown]"

      if 'permalink' in sub_dict and isinstance(sub_dict['permalink'], str):
        permalink = sub_dict['permalink'].strip()
      else:
        print("warning: could not find permalink in " + identifier)
        permalink = f'/r/{subreddit}/comments/{identifier}/foobar'

      if 'num_comments' in sub_dict:
        num_comments = sub_dict['num_comments']
      else:
        print("warning: could not find num_comments in " + identifier)
        num_comments = 0

      if 'url' in sub_dict and isinstance(sub_dict['url'], str):
        url = sub_dict['url'].strip()
      else:
        url = f'http://reddit.com/r/{subreddit}/comments/{identifier}/blah'

      if 'score' in sub_dict:
        score = sub_dict['score']
      else:
        print("warning: could not find score in " + identifier)
        score = 0

      if 'gilded' in sub_dict:
        gilded = sub_dict['gilded']
      else:
        print("warning: could not find gilded in " + identifier)
        gilded = 0

      if 'created_utc' in sub_dict:
        created_utc = sub_dict['created_utc']
      else:
        print("warning: could not find created_utc in " + identifier)
        created_utc = 0

      if 'selftext' in sub_dict and isinstance(sub_dict['selftext'], str):
        self_text = sub_dict['selftext'].strip()
      else:
        print("warning: could not find selftext in " + identifier)
        self_text = ""

      if 'is_self' in sub_dict and isinstance(sub_dict['is_self'], bool):
          is_self = sub_dict['is_self']
      else:
          print("warning: could not find is_self in " + identifier)
          # Guess if self post
          is_self = True if "reddit.com/r/" in url else False

      if 'thumbnail' in sub_dict and isinstance(sub_dict['thumbnail'], str):
        thumbnail = sub_dict['thumbnail'].strip()
      else:
        print("warning: could not find thumbnail in " + identifier)
        if is_self:
          thumbnail = "self"
        else:
          thumbnail = "default"

      print('====================')
      try:
        cursor.execute('INSERT INTO submissions(id, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s)', [identifier, subreddit, title, author, permalink, thumbnail, num_comments, url, score, gilded, created_utc, self_text, is_self])
      except Exception as error:
        print("ERROR: "+ str(error))
        print("================================")
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)
      print(f"Identifier inserted succesfully {identifier}")
conn.commit()
conn.close()
