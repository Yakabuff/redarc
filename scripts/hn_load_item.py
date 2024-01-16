import json
import time
import psycopg2
import sys
import logging
import datetime
# story: story == thread, comment == comment
# "job", "story", "comment", "poll", or "pollopt"
# job
# poll
time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
logging.basicConfig(filename='hn_items-'+time_now+'.log', encoding='utf-8', level=logging.DEBUG)

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
      item_dict = json.loads(line)

      if 'id' in item_dict and isinstance(item_dict['id'], str):
         identifier = item_dict['id'].strip()
      else:
         logging.error("Could not find ID")
         logging.debug("Line number: "+ str(line_number))
         continue

      if 'type' in item_dict and isinstance(item_dict['type'], str):
         item_type = item_dict['type'].strip().lower()
         if item_type != "story" and item_type != "comment" and item_type != "poll" and item_type != "pollopt" and item_type != "job":
            logging.error("Invalid type for: " + identifier)
            logging.debug("Line number: "+ str(line_number))
            continue
      else:
         logging.error("Could not find type for: " + identifier)
         logging.debug("Line number: "+ str(line_number))
         continue

      if 'by' in item_dict and isinstance(item_dict['by'], str):
         author = item_dict['by'].strip().lower()
      else:
         logging.warning("Could not find author in " + identifier)
         logging.debug("Line number: "+ str(line_number))
         author = "[unknown]"
       
      if item_type == "story" or item_type == "comment" or item_type == "pollopt":
         if 'score' in item_dict and isinstance(item_dict['score'], int):
            score = item_dict['score']
         elif 'score' in item_dict and isinstance(item_dict['score'], str) and item_dict['score'].isdigits():
            score = int(item_dict['score'])
         elif item_type != 'story':
            score = 0
         else:
            logging.warning("Could not find score in " + identifier)
            logging.debug("Line number: "+ str(line_number))
            score = 0
      
      if 'time' in item_dict and isinstance(item_dict['time'], int):
        created_utc = item_dict['time']
      elif 'time' in item_dict and isinstance(item_dict['time'], str) and item_dict['time'].isdigit():
        created_utc = int(item_dict['time'])
      else:
        logging.error("Could not find created_utc in " + identifier)
        logging.debug("Line number: "+ str(line_number))
        created_utc = 0

      if item_type == "story" or item_type == "comment" or item_type == "pollopt":
         if 'text' in item_dict and isinstance(item_dict['text'], str):
            # delete null chars
            text = item_dict['text'].strip().replace("\u0000", "")
         else:
            logging.warning("Could not find body in " + identifier)
            logging.debug("Line number: "+ str(line_number))
            text = ""

      if item_type == "story" or item_type == "poll" or item_type == "job":
         if 'title' in item_dict and isinstance(item_dict['title'], str):
            # delete null chars
            title = item_dict['title'].strip().replace("\u0000", "")
         else:
            logging.warning("Could not find body in " + identifier)
            logging.debug("Line number: "+ str(line_number))
            title = ""

      if item_type == "pollotp":
         if 'poll' in item_dict and isinstance(item_dict['poll'], int):
            poll = item_dict['pol']
         else:
            logging.warning("Could not find parent poll id! " + identifier)
            logging.debug("Line number: "+ str(line_number))
            continue

      if item_type == "comment":
         if 'parent' in item_dict and isinstance(item_dict['parent'], str):
            parent_id = item_dict['parent'].strip()
         else:
            logging.warning("Could not find parent in " + identifier)
            logging.debug("Line number: "+ str(line_number))

      if item_type == "story":
         if 'url' in item_dict and isinstance(item_dict['url'], str):
            url = item_dict['url'].strip()
         else:
            url = ""

      if item_type == "comment" or type == "pollopt":
         try:
            cursor.execute('INSERT INTO comments(id, subreddit, body, author, score, gilded, created_utc, parent_id, retrieved_utc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [identifier, item_type, text, author, score, created_utc, parent_id, url, int(time.time())])
         except Exception as error:
            logging.error("ERROR:" + str(error))
            logging.debug(identifier)
            logging.debug(item_type)
            logging.debug(text)
            logging.debug(author)
            logging.debug(score)
            logging.debug(created_utc)
            logging.debug(parent_id)
            continue
      elif item_type == "poll" or item_type == "job" or item_type == "story":
         try:
            cursor.execute('INSERT INTO submission(id, subreddit, body, author, score, gilded, created_utc, parent_id, link_id, retrieved_utc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', [identifier, item_type, text, author, score, created_utc, parent_id, url, int(time.time())])
         except Exception as error:
            logging.error("ERROR:" + str(error))
            logging.debug(identifier)
            logging.debug(item_type)
            logging.debug(text)
            logging.debug(author)
            logging.debug(score)
            logging.debug(created_utc)
            logging.debug(parent_id)
            logging.debug(url)
            continue
      else:
         logging.error("ERROR: invalid item type")
         continue

conn.commit()
conn.close()
