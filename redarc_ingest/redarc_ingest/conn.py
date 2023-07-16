import elasticsearch
from rq import Queue
from redis import Redis
import praw
import os
from psycopg2 import pool
import psycopg2
from dotenv import load_dotenv
load_dotenv()
redis_conn = Redis(host='localhost', port=6379)
url_queue = Queue("url_submit", connection=redis_conn)
