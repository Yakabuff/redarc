import json
import psycopg2
import sys
import logging
import datetime

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
logging.basicConfig(filename='comments-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)

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
      com_dict = json.loads(line)

      if 'id' in com_dict and isinstance(com_dict['id'], str):
        identifier = com_dict['id'].strip()
      else:
        logging.error("Could not find ID")
        logging.debug("Line number: "+ str(line_number))
        continue

      if 'subreddit' in com_dict and isinstance(com_dict['subreddit'], str):
        subreddit = com_dict['subreddit'].strip().lower()
      else:
        logging.error("Could not find subreddit for: " + identifier)
        logging.debug("Line number: "+ str(line_number))
        continue

      if 'author' in com_dict and isinstance(com_dict['author'], str):
        author = com_dict['author'].strip().lower()
      else:
        logging.warning("Could not find author in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        author = "[unknown]"
      
      if 'score' in com_dict and isinstance(com_dict['score'], int):
        score = com_dict['score']
      elif 'score' in com_dict and isinstance(com_dict['score'], str) and com_dict['score'].isdigits():
        score = int(com_dict['score'])
      else:
        logging.warning("Could not find score in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        score = 0
      
      if 'gilded' in com_dict and isinstance(com_dict['gilded'], int):
        gilded = com_dict['gilded']
      elif 'gilded' in com_dict and isinstance(com_dict['gilded'], str) and com_dict['gilded'].isdigits():
        gilded = int(com_dict['gilded'])
      else:
        logging.warning("Could not find gilded in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        gilded = 0

      if 'created_utc' in com_dict and isinstance(com_dict['created_utc'], int):
        created_utc = com_dict['created_utc']
      elif 'created_utc' in com_dict and isinstance(com_dict['created_utc'], str) and com_dict['created_utc'].isdigit():
        created_utc = int(com_dict['created_utc'])
      else:
        logging.error("Could not find created_utc in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        created_utc = 0

      if 'body' in com_dict and isinstance(com_dict['body'], str):
        # delete null chars
        body = com_dict['body'].strip().replace("\u0000", "")
      else:
        logging.warning("Could not find body in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        body = ""

      if 'link_id' in com_dict and isinstance(com_dict['link_id'], str):
        if len(com_dict['link_id'].split('_')) > 1:
          link_id = com_dict['link_id'].strip().split('_')[1]
        else:
          link_id = com_dict['link_id'].strip()
      else:
        logging.error("Could not find link_id in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        continue

      if 'parent_id' in com_dict and isinstance(com_dict['parent_id'], str):
        if len(com_dict['parent_id'].split('_')) > 1:
          parent_id = com_dict['parent_id'].strip().split('_')[1]
        else:
          parent_id = com_dict['parent_id'].strip()
      else:
        logging.warning("Could not find parent_id in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        parent_id = link_id

      try:
        cursor.execute('INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id) VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s) ON CONFLICT (id) DO NOTHING', [identifier, subreddit, body, author, score, gilded, created_utc, parent_id, link_id])
      except Exception as error:
        logging.error("ERROR:" + str(error))
        logging.debug(identifier)
        logging.debug(subreddit)
        logging.debug(body)
        logging.debug(author)
        logging.debug(score)
        logging.debug(gilded)
        logging.debug(created_utc)
        logging.debug(parent_id)
        logging.debug(link_id)
        continue
conn.commit()
conn.close()
