"""
create currencies table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE currencies"
         " ("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " name TEXT,"
         " symbol TEXT NOT NULL,"
         " volume_total_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_total_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_total NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " price_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " price_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc NUMERIC(25, 10) NOT NULL"
         ")", "DROP TABLE currencies"),
    step("CREATE INDEX currencies_symbol_idx ON currencies (symbol)", "DROP INDEX currencies_symbol_idx"),
    step("CREATE UNIQUE INDEX currencies_symbol_timestamp_epoc_idx ON currencies (symbol, timestamp_epoc)", "DROP INDEX currencies_symbol_timestamp_epoc_idx")
]
