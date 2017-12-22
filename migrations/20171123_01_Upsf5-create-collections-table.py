"""
CREATE collections table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE collections"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " path TEXT NOT NULL,"
         " meta TEXT,"
         " success BOOL NOT NULL DEFAULT false,"
         " url TEXT NOT NULL"
         ")", "DROP TABLE collections"),
    step("CREATE UNIQUE INDEX collections_path_created_at_idx ON collections (path, created_at)", "DROP INDEX collections_path_created_at_idx"),
    step("CREATE INDEX collections_path_idx ON collections (path)", "DROP INDEX collections_path_idx"),
    step("CREATE INDEX collections_url_idx ON collections (url)", "DROP INDEX collections_url_idx"),
]
