import json
import re
import sys
filename = sys.argv[1]
with open(filename) as file:
  for line in file:
      sub_dict = json.loads(line)
      type = "submission"
      if 'id' in sub_dict and isinstance(sub_dict['id'], str):
        identifier = sub_dict['id'].strip()
      elif 'name' in sub_dict and isinstance(sub_dict['name'], str) and len(sub_dict['name'].split('_')) > 1:
        identifier = sub_dict['name'].strip()
        identifier = identifier.split('_')[1]
      else:
        continue

      if 'title' in sub_dict and isinstance(sub_dict['title'], str):
        title = sub_dict['title'].strip().replace("\u0000", "")
      else:
        title = ""
      if 'selftext' in sub_dict and isinstance(sub_dict['selftext'], str):
        self_text = sub_dict['selftext'].strip().replace("\u0000", "")
      else:
        self_text = ""

      if self_text == "" and title == "":
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
        created_utc = 0

      if 'score' in sub_dict and isinstance(sub_dict['score'], int):
        score = sub_dict['score']
      elif 'score' in sub_dict and isinstance(sub_dict['score'], str) and sub_dict['score'].isdigits():
        score = int(sub_dict['score'])
      else:
        score = 0

      elastic_sub = {'title':title, 'self_text': self_text, 'score': score, 'created_utc': created_utc, 'type': type, 'subreddit': subreddit}

      meta = {"index":{"_index":"redarc","_id": identifier}}
      print(json.dumps(meta))
      print(json.dumps(elastic_sub))

