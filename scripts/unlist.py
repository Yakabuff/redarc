import json
import psycopg2
import sys
subreddit = sys.argv[1]
unlist = sys.argv[2]
if unlist == "true":
   unlist = True
else:
   unlist = False
conn = psycopg2.connect(
  database="postgres",
  user='postgres',
  password='test1234',
  host='localhost',
  port='5432'
)

cur = conn.cursor()
cur.execute("UPDATE subreddits SET unlisted = %s where name = %s", [unlist, subreddit])
conn.commit()
conn.close()