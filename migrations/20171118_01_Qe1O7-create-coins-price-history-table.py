"""
Create coins_price_history table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coins_price_history"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT NOT NULL,"
         " to_symbol TEXT NOT NULL,"
         " exchange TEXT NOT NULL,"
         " volume_from_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_to_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " close_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " open_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " low_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " high_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc BIGINT NOT NULL"
         ")", "DROP TABLE coins_price_history"),
    step("CREATE UNIQUE INDEX coins_price_history_from_to_symbol_timestamp_epoc_exchange_idx ON coins_price_history (from_symbol, to_symbol, timestamp_epoc, exchange)", "DROP INDEX coins_price_history_from_to_symbol_timestamp_epoc_exchange_idx"),
    step("CREATE INDEX coins_price_history_from_symbol_idx ON coins_price_history (from_symbol)", "DROP INDEX coins_price_history_from_symbol_idx"),
    step("CREATE INDEX coins_price_history_to_symbol_idx ON coins_price_history (to_symbol)", "DROP INDEX coins_price_history_to_symbol_idx")
]
