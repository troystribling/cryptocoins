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
         " algorithm TEXT,"
         " proof_type TEXT,"
         " block_number BIGINT,"
         " net_hashes_per_second NUMERIC(46, 21),"
         " total_coins_mined NUMERIC(41, 21),"
         " block_reward NUMERIC(41, 21),"
         " volume_from_24_hour NUMERIC(41, 21),"
         " volume_to_24_hour NUMERIC(41, 21),"
         " open_price_24_hour NUMERIC(41, 21),"
         " close_price_24_hour NUMERIC(41, 21),"
         " low_price_24_hour NUMERIC(41, 21),"
         " high_price_24_hour NUMERIC(41, 21),"
         " timestamp_epoc BIGINT NOT NULL,"
         " last_update_epoc BIGINT NOT NULL"
         ")", "DROP TABLE coins_history"),
    step("CREATE INDEX coins_history_from_symbol_idx ON coins_history (from_symbol)", "DROP INDEX coins_history_from_symbol_idx"),
    step("CREATE INDEX coins_history_to_symbol_idx ON coins_history (to_symbol)", "DROP INDEX coins_history_to_symbol_idx"),
    step("CREATE INDEX coins_history_from_symbol_to_symbol_idx ON coins_history (from_symbol, to_symbol)", "DROP INDEX coins_history_from_symbol_to_symbol_idx"),
]
