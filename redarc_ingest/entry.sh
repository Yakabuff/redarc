#!/bin/bash

# Generate .env with envars
cd /ingest/redarc_ingest
echo "INGEST_ENABLED=$INGEST_ENABLED" > .env
cd /ingest/worker
echo "PG_DATABASE=postgres
PG_USER=postgres
PG_PASSWORD=$PG_PASSWORD
PG_HOST=$PG_HOST
PG_PORT=$PG_PORT

CLIENT_ID=$CLIENT_ID
CLIENT_SECRET=$CLIENT_SECRET
PASSWORD=$PASSWORD
USER_AGENT=$USER_AGENT
REDDIT_USERNAME=$REDDIT_USERNAME
INDEX_DELAY=$INDEX_DELAY
INGEST_PASSWORD=$INGEST_PASSWORD" > .env

cd /ingest

redis-server &

# Start gunicorn
gunicorn -b 0.0.0.0:8000 --reload redarc_ingest.app &

if [ "$INGEST_ENABLED" = "true" ] ; then
   echo "ingest enabled"
   # Start reddit worker
   python3 -m worker.reddit_worker &

   # Start index worker
   python3 -m worker.index_worker &
fi
wait