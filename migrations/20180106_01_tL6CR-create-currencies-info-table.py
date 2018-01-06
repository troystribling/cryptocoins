"""
create_currencies_info table
"""

from yoyo import step

__depends__ = {'20171110_01_sMLWW-create-coins-table'}

steps = [
    step("CREATE TABLE currencies_info"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " symbol TEXT NOT NULL,"
         " name TEXT,"
         " description TEXT"
         ")", "DROP TABLE currencies_info"),
    step("CREATE UNIQUE INDEX currencies_info_symbol_idx ON currencies_info (symbol)", "DROP INDEX currencies_info_symbol_idx")
]
