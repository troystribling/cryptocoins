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
         " path TEXT NOT NULL,"
         " file_name TEXT NOT NULL,"
         " date_dir TEXT NOT NULL,"
         " success BOOL NOT NULL DEFAULT false"
         ")", "DROP TABLE imports"),
    step("CREATE UNIQUE INDEX imports_file_name_idx ON imports (file_name)", "DROP INDEX imports_file_name_idx")
]
