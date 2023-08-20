import os
# import praw
from dotenv import load_dotenv
from psycopg2 import pool
import psycopg2
load_dotenv()

pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                        password=os.getenv('PG_PASSWORD'),
                                                        host=os.getenv('PG_HOST'),
                                                        port=os.getenv('PG_PORT'),
                                                        database=os.getenv('PG_DATABASE'))

pg_pool_fts = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PGFTS_USER'),
                                                        password=os.getenv('PGFTS_PASSWORD'),
                                                        host=os.getenv('PGFTS_HOST'),
                                                        port=os.getenv('PGFTS_PORT'),
                                                        database=os.getenv('PGFTS_DATABASE'))