"""
create forex-pairs-history
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE forex_pairs_history"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT NOT NULL,"
         " to_symbol TEXT NOT NULL,"
         " price NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc BIGINT NOT NULL"
         ")", "DROP TABLE forex_pairs_history"),
    step("CREATE INDEX forex_pairs_history_from_symbol_idx ON forex_pairs_history (from_symbol)", "DROP INDEX forex_pairs_history_from_symbol_idx"),
    step("CREATE UNIQUE INDEX forex_pairs_history_from_to_symbol_timestamp_epoc_idx ON forex_pairs_history (from_symbol, to_symbol, timestamp_epoc)", "DROP INDEX forex_pairs_history_from_to_symbol_timestamp_epoc_idx")
]
