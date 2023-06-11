import os

POSTGRES_PASSWORD = os.environ["PGPASSWORD"]
ES_PASSWORD = os.environ["ES_PASSWORD"]
ES_HOST = os.environ["ES_HOST"]
ES_ENABLED = os.environ["ES_ENABLED"]

with open("config.json") as f:
    newText=f.read().replace('test1234', POSTGRES_PASSWORD)
    newText=newText.replace('$ES_PASSWORD', ES_PASSWORD)
    newText=newText.replace('$ES_HOST', ES_HOST)
    newText=newText.replace('"$ES_ENABLED"', ES_ENABLED)
with open("config.json", "w") as f:
    f.write(newText)
