ALTER TABLE comments ADD COLUMN retrieved_utc bigint NOT NULL;
ALTER TABLE submissions ADD COLUMN retrieved_utc bigint NOT NULL;
// todo