import os

POSTGRES_PASSWORD = os.environ["PGPASSWORD"]
POSTGRESFTS_PASSWORD = os.environ["PGPASSWORD"]

if "ADMIN_PASSWORD" in os.environ:
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
else:
    ADMIN_PASSWORD = "asdf"

with open("config.json") as f:
    newText=f.read().replace('test1234', POSTGRES_PASSWORD)
    newText=newText.replace('test1234fts', POSTGRESFTS_PASSWORD)
    newText=newText.replace('$ADMIN_PASSWORD', ADMIN_PASSWORD)
with open("config.json", "w") as f:
    f.write(newText)
