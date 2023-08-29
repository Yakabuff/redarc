#!/bin/bash

# Database setup
export PGPASSWORD=$PG_PASSWORD
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_submissions.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_comments.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_subreddits.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_comments_index.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_submissions_index.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_status_comments.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_status_submissions.sql
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_progress.sql
unset PGPASSWORD
export PGPASSWORD=$PGFTS_PASSWORD
psql -h pgsql-fts -U postgres -p $PGFTS_PORT -a -f scripts/db_fts.sql

# Update postgres password
cd /redarc/api
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

INGEST_PASSWORD=$INGEST_PASSWORD
INGEST_ENABLED=$INGEST_ENABLED
ADMIN_PASSWORD=$ADMIN_PASSWORD
REDIS_HOST=$REDIS_HOST" > .env
# Start API
gunicorn app &

# Build react frontend
cd /redarc/frontend
echo "VITE_API_DOMAIN=$REDARC_API" > .env
npm run build

# Move assets to NGINX
mkdir -p /var/www/html/redarc/
cp -R dist/* /var/www/html/redarc/

# NGINX config
cd /redarc/nginx
python3 nginx_envar.py
mv redarc.conf /etc/nginx/http.d/redarc.conf

# Start nginx
nginx -g "daemon off;"