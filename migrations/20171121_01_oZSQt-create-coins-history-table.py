"""
CREATE coin_history table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coins_history"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT NOT NULL,"
         " to_symbol TEXT NOT NULL,"
         " algorithm TEXT NULL,"
         " proof_type TEXT NULL,"
         " block_number BIGINT NOT NULL,"
         " net_hashes_per_second NUMERIC(46, 21) NOT NULL,"
         " total_coins_mined NUMERIC(41, 21) NOT NULL,"
         " block_reward NUMERIC(41, 21) NOT NULL,"
         " volume_from_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " volume_to_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " open_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " close_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " low_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " high_price_24_hour NUMERIC(41, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc BIGINT NOT NULL,"
         " timestamp TIMESTAMP NOT NULL"
         ")", "DROP TABLE coins_history"),
    step("CREATE INDEX coins_history_from_symbol_idx ON coins_history (from_symbol)", "DROP INDEX coins_history_from_symbol_idx"),
    step("CREATE INDEX coins_history_to_symbol_idx ON coins_history (to_symbol)", "DROP INDEX coins_history_to_symbol_idx"),
    step("CREATE INDEX coins_history_from_symbol_to_symbol_idx ON coins_history (from_symbol, to_symbol)", "DROP INDEX coins_history_from_symbol_to_symbol_idx"),
]
