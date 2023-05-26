import os
import sys
print(sys.argv)
REDARC_API = sys.argv[1]
SERVER_NAME = sys.argv[2]
with open("redarc_original.conf") as f:
    newText=f.read().replace('$REDARC_API', REDARC_API)
    newText=newText.replace('$SERVER_NAME', SERVER_NAME)

with open("redarc.conf", "w") as f:
    f.write(newText)
