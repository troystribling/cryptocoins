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
         " name TEXT NOT NULL,"
         " url TEXT NOT NULL"
         ")", "DROP TABLE imports"),
    step("CREATE INDEX collections_name_idx ON collections (name)", "DROP INDEX collections_name_idx")
]
