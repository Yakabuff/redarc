import os

POSTGRES_PASSWORD = os.environ["PGPASSWORD"]

if "ES_PASSWORD" in os.environ:
    ES_PASSWORD = os.environ["ES_PASSWORD"]
else: 
    ES_PASSWORD = ""

if "ES_HOST" in os.environ:
    ES_HOST = os.environ["ES_HOST"]
else:
    ES_HOST = "http://invalid.localhost"

if "ES_ENABLED" in os.environ:
    ES_ENABLED = os.environ["ES_ENABLED"]
else:
    ES_ENABLED = "false"

if "ADMIN_PASSWORD" in os.environ:
    ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
else:
    ADMIN_PASSWORD = "asdf"

with open("config.json") as f:
    newText=f.read().replace('test1234', POSTGRES_PASSWORD)
    newText=newText.replace('$ES_PASSWORD', ES_PASSWORD)
    newText=newText.replace('$ES_HOST', ES_HOST)
    newText=newText.replace('"$ES_ENABLED"', ES_ENABLED)
    newText=newText.replace('$ADMIN_PASSWORD', ADMIN_PASSWORD)
with open("config.json", "w") as f:
    f.write(newText)
