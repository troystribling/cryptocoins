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
         " updated_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " coin_name TEXT NOT NULL,"
         " full_name TEXT NOT NULL,"
         " cryptocompare_id BIGINT NOT NULL,"
         " name TEXT NOT NULL,"
         " symbol TEXT NOT NULL,"
         " rank BIGINT NOT NULL DEFAULT 1"
         ")", "DROP TABLE COINS"),
    step("CREATE UNIQUE INDEX coins_symbol_idx ON coins (symbol)", "DROP INDEX coins_symbol_idx")
]
