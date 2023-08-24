CREATE INDEX IF NOT EXISTS submissions_subreddit_idx on submissions(subreddit);

CREATE INDEX IF NOT EXISTS submissions_created_timestamp_idx on submissions(created_utc);

CREATE INDEX IF NOT EXISTS submissions_timestamp_idx on submissions(created_utc, retrieved_utc);