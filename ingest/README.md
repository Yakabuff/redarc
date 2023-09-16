# redarc-ingest

### Image downloader:
- Downloads images queued by the Reddit worker

### Reddit worker:
- Fetches threads and comments and queues images to be downloaded

### Subreddit worker:
- Retrieves hot/new/rising threads and queues them for Reddit worker to process periodically

### Index worker:
- Periodically indexes the databases