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
      if 'name' in sub_dict:
        identifier = sub_dict['name'].strip()
      else:
          identifier = sub_dict['id'].strip()
      subreddit = sub_dict['subreddit'].strip()
      title = sub_dict['title'].strip()
      author = sub_dict['author'].strip()
      permalink = sub_dict['permalink'].strip()
      thumbnail = sub_dict['thumbnail'].strip()
      num_comments = sub_dict['num_comments']
      if 'url' in sub_dict and sub_dict['url'] != None:
        url = sub_dict['url'].strip()
      else:
         url = permalink
      score = sub_dict['score']
      gilded = sub_dict['gilded']
      created_utc = sub_dict['created_utc']
      self_text = sub_dict['selftext'].strip()
      is_self = sub_dict['is_self']
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
