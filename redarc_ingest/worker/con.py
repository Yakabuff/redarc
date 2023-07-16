import os
import praw
from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    password=os.getenv('PASSWORD'),
    user_agent=os.getenv('USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
)

pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                        password=os.getenv('PG_PASSWORD'),
                                                        host=os.getenv('PG_HOST'),
                                                        port=os.getenv('PG_PORT'),
                                                        database=os.getenv('PG_DATABASE'))