CREATE INDEX IF NOT EXISTS comments_link_id_idx on comments(link_id);
CREATE INDEX IF NOT EXISTS comments_parent_id_idx on comments(parent_id);
CREATE INDEX IF NOT EXISTS comments_subreddit_idx on comments(subreddit);

CREATE INDEX IF NOT EXISTS comments_created_timestamp_idx on comments(created_utc);
CREATE INDEX IF NOT EXISTS comments_timestamp_idx on comments(created_utc, retrieved_utc);