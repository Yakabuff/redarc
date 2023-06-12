#!/bin/bash

# $1 is name of subreddit
# $2 is filename of submission dump
# $3 is filename of comment dump
# $4 is elasticsearch password
PW=$4

DIRECTORY=.
python3 scripts/es_ingest_submission.py $2 > $1_es_sub_processed
python3 scripts/es_ingest_comment.py $3 > $1_es_com_processed

split --verbose -l300000 $1_es_sub_processed $1_es_sub.
split --verbose -l300000 $1_es_com_processed $1_es_com.

for i in $DIRECTORY/$1_es_sub.*; do
    curl -u elastic:$PW -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/_bulk' --data-binary @$i
done

for i in $DIRECTORY/$1_es_com.*; do
    curl -u elastic:$PW -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/_bulk' --data-binary @$i
done