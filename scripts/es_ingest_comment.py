import json
import re
import sys
filename = sys.argv[1]
with open(filename) as file:
  for line in file:
      sub_dict = json.loads(line)
      type = "comment"
      if 'id' in sub_dict and isinstance(sub_dict['id'], str):
        identifier = sub_dict['id'].strip()
      elif 'name' in sub_dict and isinstance(sub_dict['name'], str) and len(sub_dict['name'].split('_')) > 1:
        identifier = sub_dict['name'].strip()
        identifier = identifier.split('_')[1]
      else:
        continue 

      if 'body' in sub_dict and isinstance(sub_dict['body'], str):
        body = sub_dict['body'].strip().replace("\u0000", "")
      else:
        continue 

      if 'subreddit' in sub_dict and isinstance(sub_dict['subreddit'], str):
        subreddit = sub_dict['subreddit'].strip().replace("\u0000", "").lower()
      else:
        continue

      if 'created_utc' in sub_dict and isinstance(sub_dict['created_utc'], int):
        created_utc = sub_dict['created_utc']
      elif 'created_utc' in sub_dict and isinstance(sub_dict['created_utc'], str) and sub_dict['created_utc'].isdigit():
        created_utc = int(sub_dict['created_utc'])
      else:
        continue

      if 'link_id' in sub_dict and isinstance(sub_dict['link_id'], str):
        if len(sub_dict['link_id'].split('_')) > 1:
          link_id = sub_dict['link_id'].strip().split('_')[1]
        else:
          link_id = sub_dict['link_id'].strip()
      else:
        continue

      if 'score' in sub_dict and isinstance(sub_dict['score'], int):
        score = sub_dict['score']
      elif 'score' in sub_dict and isinstance(sub_dict['score'], str) and sub_dict['score'].isdigits():
        score = int(sub_dict['score'])
      else:
        score = 0

      elastic_com = {"body": body, "score": score, "created_utc": created_utc, "type": type, "subreddit": subreddit, "link_id": link_id}
      meta = {"index":{"_index":"redarc_comments","_id": identifier}}
      print(json.dumps(meta))
      print(json.dumps(elastic_com))


