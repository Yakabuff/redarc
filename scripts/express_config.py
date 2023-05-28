import os

POSTGRES_PASSWORD = os.environ["PGPASSWORD"]

with open("config.json") as f:
    newText=f.read().replace('test1234', POSTGRES_PASSWORD)

with open("config.json", "w") as f:
    f.write(newText)
