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
         " remote_dir TEXT,"
         " file_name TEXT,"
         " date_dir TEXT"
         ")", "DROP TABLE imports"),
    step("CREATE UNIQUE INDEX imports_file_name_idx ON imports (file_name)", "DROP INDEX imports_file_name_idx")
]
