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

      if 'id' in com_dict and isinstance(com_dict['id'], str):
        identifier = com_dict['id'].strip()
      else:
        print("error: could not find ID")
        print("================================")
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)

      if 'subreddit' in com_dict and isinstance(com_dict['subreddit'], str):
        subreddit = com_dict['subreddit'].strip()
      else:
        print("error: could not find subreddit for identifier " + identifier)
        print("================================")
        cursor.execute('ROLLBACK;')
        conn.close()
        sys.exit(1)

      if 'author' in com_dict and isinstance(com_dict['author'], str):
        author = com_dict['author'].strip()
      else:
        print("warning: could not find author in " + identifier)
        author = "[unknown]"
      
      if 'score' in com_dict:
        score = com_dict['score']
      else:
        print("warning: could not find score in " + identifier)
        score = 0
      
      if 'gilded' in com_dict:
        gilded = com_dict['gilded']
      else:
        print("warning: could not find gilded in " + identifier)
        gilded = 0

      if 'created_utc' in com_dict:
        created_utc = com_dict['created_utc']
      else:
        print("warning: could not find created_utc in " + identifier)
        created_utc = 0

      if 'body' in com_dict and isinstance(com_dict['body'], str):
        # delete null chars
        body = com_dict['body'].strip().replace("\u0000", "")
      else:
        print("warning: could not find body in " + identifier)
        body = ""

      if 'link_id' in com_dict and isinstance(com_dict['link_id'], str):
        link_id = com_dict['link_id'].strip()
      else:
        print("warning: could not find link_id in " + identifier)
        link_id = ""

      if 'parent_id' in com_dict and isinstance(com_dict['parent_id'], str):
        parent_id = com_dict['parent_id'].strip()
      else:
        print("warning: could not find parent_id in " + identifier)
        parent_id = link_id

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
