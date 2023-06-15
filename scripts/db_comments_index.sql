CREATE INDEX IF NOT EXISTS comments_link_id_idx on comments(link_id);
CREATE INDEX IF NOT EXISTS comments_parent_id_idx on comments(parent_id);
CREATE INDEX IF NOT EXISTS comments_subreddit_idx on comments(subreddit);