#!/bin/bash

cd /ingest

redis-server &

if [ "$INGEST_ENABLED" = "true" ] ; then
   echo "ingest enabled"
   # Start reddit worker
   python3 -m worker.reddit_worker &

   python3 -m worker.subreddit_worker &

   python3 -m worker.image_downloader &
fi

if [ "$INDEX_ENABLED" = "true" ] ; then
   echo "index enabled"
   # Start index worker
   python3 -m worker.index_worker &
fi
wait