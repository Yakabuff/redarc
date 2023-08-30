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
PGFTS_DATABASE=postgres
PGFTS_USER=postgres
PGFTS_PASSWORD=$PGFTS_PASSWORD
PGFTS_HOST=$PGFTS_HOST
PGFTS_PORT=$PGFTS_PORT
CLIENT_ID=$CLIENT_ID
CLIENT_SECRET=$CLIENT_SECRET
PASSWORD=$PASSWORD
USER_AGENT=$USER_AGENT
REDDIT_USERNAME=$REDDIT_USERNAME
INDEX_DELAY=$INDEX_DELAY
INGEST_PASSWORD=$INGEST_PASSWORD" > .env

cd /ingest

redis-server &

if [ "$INGEST_ENABLED" = "true" ] ; then
   echo "ingest enabled"
   # Start reddit worker
   python3 -m worker.reddit_worker &
fi

if [ "$INDEX_ENABLED" = "true" ] ; then
   echo "index enabled"
   # Start index worker
   python3 -m worker.index_worker &
fi
wait