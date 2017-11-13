"""
CREATE import table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE imports"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " remote_path TEXT"
         ")", "DROP TABLE imports"),
    step("CREATE UNIQUE INDEX import_remote_path_idx ON imports (remote_path)", "DROP INDEX import_remote_path_idx")
]
