import json
import psycopg2
import sys

conn = psycopg2.connect(
  database="postgres",
  user='postgres',
  password='test1234',
  host='localhost',
  port='5432'
)

cur = conn.cursor()
cur.execute("select DISTINCT subreddit from submissions;")
subreddits = cur.fetchall()

for row in subreddits:
  print(f"INDEXING: {row[0]}")
  cur.execute("select COUNT(*) from submissions where subreddit = %s;", (row))
  num_submissions = cur.fetchone()

  cur.execute("select COUNT(*) from comments where subreddit = %s;", (row))
  num_comments = cur.fetchone()

  cur.execute("INSERT INTO subreddits (name, unlisted, num_submissions, num_comments) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET(num_submissions, num_comments) = (%s, %s)",(row, False, num_submissions, num_comments, num_submissions, num_comments))
  conn.commit()

conn.close()
