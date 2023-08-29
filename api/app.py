import falcon
import os
from psycopg2 import pool
import psycopg2
from rq import Queue
from redis import Redis
from submit import Submit
from comments import Comments
from subreddits import Subreddits
from progress import Progress
from submissions import Submissions
from status import Status
from search import Search
from dotenv import load_dotenv
load_dotenv()

app = application = falcon.App(cors_enable=True)
pg_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PG_USER'),
                                                      password=os.getenv('PG_PASSWORD'),
                                                      host=os.getenv('PG_HOST'),
                                                      port=os.getenv('PG_PORT'),
                                                      database=os.getenv('PG_DATABASE'))

pgfts_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.getenv('PGFTS_USER'),
                                                      password=os.getenv('PGFTS_PASSWORD'),
                                                      host=os.getenv('PGFTS_HOST'),
                                                      port=os.getenv('PGFTS_PORT'),
                                                      database=os.getenv('PGFTS_DATABASE'))

redis_conn = Redis(host=os.getenv('REDIS_HOST'), port=6379)
url_queue = Queue("url_submit", connection=redis_conn)

comments = Comments(pg_pool)
subreddits = Subreddits(pg_pool)
progress = Progress(pg_pool)
submissions = Submissions(pg_pool)
submit = Submit(url_queue)
status = Status(pg_pool)
search = Search(pgfts_pool)

app.add_route('/submit', submit)
app.add_route('/search/comments', comments)
app.add_route('/search/submissions', submissions)
app.add_route('/search/subreddits', subreddits)
app.add_route('/search', search)
app.add_route('/progress', progress)
app.add_route('/status', status)