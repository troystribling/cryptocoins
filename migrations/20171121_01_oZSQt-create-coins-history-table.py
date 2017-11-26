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
         " symbol TEXT NOT NULL,"
         " algorithm TEXT NOT NULL,"
         " proof_type TEXT NOT NULL,"
         " block_number BIGINT NOT NULL,"
         " net_hashes_per_second NUMERIC(21, 21) NOT NULL,"
         " total_coins_mined NUMERIC(21, 21) NOT NULL,"
         " block_reward NUMERIC(21, 21) NOT NULL,"
         " volume_from_24_hour NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " volume_to_24_hour NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " open_price_24_hour NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " low_price_24_hour NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " high_price_24_hour NUMERIC(21, 21) NOT NULL DEFAULT 0.0,"
         " timestamp_epoc BIGINT NOT NULL,"
         " timestamp TIMESTAMP NOT NULL"         
         ")", "DROP TABLE coins_history"),
    step("CREATE INDEX coins_history_symbol_idx ON coins_history (symbol)", "DROP INDEX coins_history_symbol_idx")
]
