#!/bin/bash
cd /redarc

# Database setup
psql -h pgsql-dev -U postgres -a -f scripts/db_submissions.sql
psql -h pgsql-dev -U postgres -a -f scripts/db_comments.sql
psql -h pgsql-dev -U postgres -a -f scripts/db_subreddits.sql
psql -h pgsql-dev -U postgres -a -f scripts/db_comments_index.sql
psql -h pgsql-dev -U postgres -a -f scripts/db_submissions_index.sql

# Update postgres password
python3 scripts/express_config.py
# Start API
node server.js &

# Build react frontend
cd /redarc/redarc-frontend
echo "VITE_API_DOMAIN=$REDARC_API" > .env
npm run build

# Move assets to NGINX
mkdir -p /var/www/html/redarc/
cp -R dist/* /var/www/html/redarc/

# NGINX config
cd /redarc/nginx
python3 nginx_envar.py $REDARC_API $SERVER_NAME
mv redarc.conf /etc/nginx/http.d/redarc.conf

# Start nginx
nginx -g "daemon off;"