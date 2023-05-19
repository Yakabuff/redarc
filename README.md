# redarc
1) Download dumps from pushshift

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

2) Provision Postgres database 

```
docker pull postgres
docker run \
  --name pgsql-dev \
  –rm \
  -e POSTGRES_PASSWORD=test1234 \
  -p 5432:5432 postgres
```

```
psql -h localhost -U postgres -a -f db.sql
psql -h localhost -U postgres -a -f db2.sql
```

3) Process dump and insert rows into postgres database with the load_sub/load_comments scripts

```
python3 load_sub.py submission_file.txt
python3 load_comments.py comment_file.txt
```

4) Start the API server.

```
npm i
node server.js
```

5) Start the frontend

```
cd redarc-frontend
npm i
npm run dev // Dev server
npm run build // Deploy
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