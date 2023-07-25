import os
import sys

REDARC_API = os.environ['REDARC_API']
SERVER_NAME = os.environ['SERVER_NAME']
REDARC_SUBMIT = os.environ['REDARC_SUBMIT']
with open("redarc_original.conf") as f:
    newText=f.read().replace('$REDARC_API', REDARC_API)
    newText=newText.replace('$SERVER_NAME', SERVER_NAME)
    newText=newText.replace('$REDARC_SUBMIT', REDARC_SUBMIT)

with open("redarc.conf", "w") as f:
    f.write(newText)
