# redarc
Here's how you can host your own Reddit archive.
### Download pushshift dumps

```
https://the-eye.eu/redarcs/
```
All data 2005-06 to 2022-12:
```
magnet:?xt=urn:btih:7c0645c94321311bb05bd879ddee4d0eba08aaee&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce
```
Top 20,000 subreddits:
```
magnet:?xt=urn:btih:c398a571976c78d346c325bd75c47b82edf6124e&tr=https%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce
```

# Docker (Recommended)

Install Docker: https://docs.docker.com/engine/install

The following commands must be run in order.

If you wish to change the postgres password, make sure `POSTGRES_PASSWORD` and `PGPASSWORD` are the same.

If you are using redarc on your personal machine, set docker envars `REDARC_API=http://localhost/api` and `SERVER_NAME=localhost`.

`REDARC_API` is the URL of your API server; it must end with `/api` 
eg: `http://redarc.basedbin.org/api`.  

`SERVER_NAME` is the URL your redarc instance is running on. eg: `redarc.basedbin.org`

```
$ docker network create redarc

$ docker pull postgres

$ docker run \
  --name pgsql-dev \
  --network redarc \
  -e POSTGRES_PASSWORD=test1234 \
  -d \
  -v ${PWD}/postgres-docker:/var/lib/postgresql/data \
  -p 5432:5432 postgres 

$ docker build . -t redarc

$ docker run --network redarc -e REDARC_API=http://redarc.mysite.org/api/ -e SERVER_NAME=redarc.mysite.org -e PGPASSWORD=test1234 -d -p 80:80 -it redarc 
```

Ensure Python3 and PIP are installed:
```
python3 scripts/load_sub.py <submission_file.txt>
python3 scripts/load_comments.py <comment_file.txt>
python3 scripts/index.py [subreddit_name]
# Optional
python3 scripts/unlist.py <subreddit> <true|false>
```


# Manual installation:

### 1) Provision Postgres database 

```
$ docker pull postgres
$ docker run \
  --name pgsql-dev \
  -e POSTGRES_PASSWORD=test1234 \
  -d \
  -v ${PWD}/postgres-docker:/var/lib/postgresql/data \
  -p 5432:5432 postgres 
```

```
psql -h localhost -U postgres -a -f db_submissions.sql
psql -h localhost -U postgres -a -f db_comments.sql
psql -h localhost -U postgres -a -f db_subreddits.sql
```

### 2) Process dump and insert rows into postgres database with the load_sub/load_comments scripts

```
python3 load_sub.py <submission_file.txt>
python3 load_comments.py <comment_file.txt>
python3 index.py [subreddit_name]
python3 unlist.py <subreddit> <true|false>
```

### 3) Start the API server.

```
npm i
node server.js
OR
pm2 start server.js
```

### 4) Start the frontend

```
mv sample.env .env
```
Set address for API server in the .env file

```
VITE_API_DOMAIN=http://my-api-server.com
```

```
cd redarc-frontend
npm i
npm run dev // Dev server
```

### 5) Provision NGINX (Optional)

/etc/nginx/conf.d/redarc.conf

```
server{
    listen 80;
    listen [::]:80;
    server_name example.com;
    location ^~ /api/ {
        proxy_redirect http://localhost:3000 http://example.com/api/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header Upgrade $http_upgrade;
        proxy_http_version 1.1;
    }
    root /var/www/html/redarc;
    index index.html;
    location / {
    try_files $uri /index.html;
    }
}
```
```
cd redarc-frontend
npm run build 
cp -R dist/* /var/www/html/redarc/
systemctl restart nginx
```

# API:

`search/comments?`
- `[unflatten = <True/False>]`
- `[subreddit = <name>]`
- `[author = <name>]`
- `[id = <id>]`
- `[body = <content>]`
- `[before = <utc_timestamp>]`
- `[after = <utc_timestamp>]`
- `[parent_id = <parent_id>]`
- `[link_id = <link_id>]`
- `[sort = <ASC/DESC>]`

`search/submissions?`
- `[subreddit = <name>]`
- `[author = <name>]`
- `[id = <id>]`
- `[title = <title>]`
- `[before = <utc_timestamp>]`
- `[after = <utc_timestamp>]`
- `[sort = <ASC/DESC>]`

`search/subreddits`