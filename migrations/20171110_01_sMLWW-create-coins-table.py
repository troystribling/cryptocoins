"""
CREATE coins table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coins"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " coin_name TEXT,"
         " full_name TEXT,"
         " cryptocompare_id BIGINT,"
         " name TEXT,"
         " symbol TEXT,"
         " url TEXT"
         ")", "DROP TABLE COINS"),
    step("CREATE UNIQUE INDEX coins_symbol_idx ON coins (symbol)", "DROP INDEX coins_symbol_idx")
]
