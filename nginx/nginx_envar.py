import os

REDARC_API = os.environ['REDARC_API']
SERVER_NAME = os.environ['SERVER_NAME']
with open("redarc_original.conf") as f:
    newText=f.read().replace('$REDARC_API', REDARC_API)
    newText=newText.replace('$SERVER_NAME', SERVER_NAME)

with open("redarc.conf", "w") as f:
    f.write(newText)
