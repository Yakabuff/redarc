# redarc API
1) Download dumps from pushshift
2) Provision Postgres database 
psql -h localhost -U postgres -a -f db.sql
psql -h localhost -U postgres -a -f db2.sql
3) Process dump and insert rows into postgres database with the load_sub/load_comments scripts
4) Make queries with the API
