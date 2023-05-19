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
      com_dict = json.loads(line)
      identifier = com_dict['id'].strip()
      subreddit = com_dict['subreddit'].strip()
      author = com_dict['author'].strip()
      score = com_dict['score']
      gilded = com_dict['gilded']
      created_utc = com_dict['created_utc']
      body = com_dict['body'].strip().replace("\u0000", "")
      parent_id = com_dict['parent_id'].strip()
      link_id = com_dict['link_id'].strip()
      print('====================')
      try:
        cursor.execute('INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id) VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING', [identifier, subreddit, body, author, score, gilded, created_utc, parent_id, link_id])
      except Exception as error:
        print("ERROR:" + str(error))
        print(identifier)
        print(subreddit)
        print(body)
        print(author)
        print(score)
        print(gilded)
        print(created_utc)
        print(parent_id)
        print(link_id)
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)

      print(f"Identifier inserted succesfully {identifier}")
conn.commit()
conn.close()
