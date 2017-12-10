"""
CREATE exchanges_history table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE exchanges_history"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT NOT NULL,"
         " to_symbol TEXT NOT NULL,"
         " name TEXT NOT NULL,"
         " volume_from_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_to_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " open_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " close_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " low_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " high_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc BIGINT NOT NULL,"
         " timestamp TIMESTAMP NOT NULL"
         ")", "DROP TABLE exchanges_history"),
    step("CREATE INDEX exchanges_history_name_idx ON exchanges_history (name)", "DROP INDEX exchanges_history_name_idx")
]
