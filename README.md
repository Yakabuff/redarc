# redarc API
1) Download dumps from pushshift
https://files.pushshift.io/reddit/
https://the-eye.eu/redarcs/
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
4) Make queries with the API
