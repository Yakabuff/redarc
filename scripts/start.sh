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
psql -h pgsql-dev -U postgres -p $PG_PORT -a -f scripts/db_watchedsubreddits.sql
unset PGPASSWORD
export PGPASSWORD=$PGFTS_PASSWORD
psql -h pgsql-fts -U postgres -p $PGFTS_PORT -a -f scripts/db_fts.sql

cd /redarc/api
# Start API
gunicorn --workers=4 app &

# Build react frontend
cd /redarc/frontend
echo "VITE_API_DOMAIN=$REDARC_FE_API" > .env
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