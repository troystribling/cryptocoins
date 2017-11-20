"""
CREATE exchanges table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE exchanges"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " name TEXT NOT NULL,"
         " volume_usd NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " rank BIGINT NOT NULL DEFAULT 1"
         ")", "DROP TABLE exchanges"),
    step("CREATE UNIQUE INDEX exchanges_name_idx ON exchanges (name)", "DROP INDEX exchanges_name_idx")
]
