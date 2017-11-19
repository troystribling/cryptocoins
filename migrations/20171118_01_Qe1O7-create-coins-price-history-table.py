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
         " from_symbol TEXT,"
         " to_symbol TEXT,"
         " volume_from NUMERIC(21, 21),"
         " volume_to NUMERIC(21, 21),"
         " close_price NUMERIC(21, 21),"
         " open_price NUMERIC(21, 21),"
         " low_price NUMERIC(21, 21),"
         " high_price NUMERIC(21, 21),"
         " timestamp BIGINT"
         ")", "DROP TABLE coins_price_history"),
    step("CREATE INDEX coins_price_history_from_to_symbol_timestamp_idx ON coins_price_history (from_symbol, to_symbol, timestamp)", "DROP INDEX coins_price_history_from_to_symbol_timestamp_idx"),
    step("CREATE INDEX coins_price_history_from_symbol_idx ON coins_price_history (from_symbol)", "DROP INDEX coins_price_history_from_symbol_idx"),
    step("CREATE INDEX coins_price_history_to_symbol_idx ON coins_price_history (to_symbol)", "DROP INDEX coins_price_history_to_symbol_idx")
]
