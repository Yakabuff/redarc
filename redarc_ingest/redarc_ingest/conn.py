from rq import Queue
from redis import Redis

redis_conn = Redis(host='localhost', port=6379)
url_queue = Queue("url_submit", connection=redis_conn)
