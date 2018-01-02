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
         " coin_name TEXT NOT NULL,"
         " full_name TEXT NOT NULL,"
         " cryptocompare_id BIGINT NOT NULL,"
         " name TEXT NOT NULL,"
         " symbol TEXT NOT NULL,"
         " volume_total_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_total_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_total NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " price_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " price_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " marketcap_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " marketcap_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " spread_usd NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " spread_btc NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " crypto_compare_rank BIGINT NOT NULL DEFAULT 1,"
         " timestamp_epoc NUMERIC(25, 10) NOT NULL"
         ")", "DROP TABLE coins"),
    step("CREATE INDEX coins_symbol_idx ON coins (symbol)", "DROP INDEX coins_symbol_idx"),
    step("CREATE UNIQUE INDEX coins_symbol_timestamp_epoc_idx ON coins (symbol, timestamp_epoc)", "DROP INDEX coins_symbol_timestamp_epoc_idx")
]
