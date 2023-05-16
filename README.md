# redarc
1) Download dumps from pushshift

```
https://the-eye.eu/redarcs/
```

2) Provision Postgres database 

```
psql -h localhost -U postgres -a -f db.sql
psql -h localhost -U postgres -a -f db2.sql
```

3) Process dump and insert rows into postgres database with the load_sub/load_comments scripts

```
python3 load_sub.py
python3 load_comments.py
```

4) Start the API server.

```
npm i
node server.js
```

5) Start the frontend

TODO: instructions

```
cd redarc-frontend
npm i
npm run dev
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