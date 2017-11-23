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
         " block_reward NUMERIC(21, 21) NOT NULL"
         ")", "DROP TABLE coins_history"),
    step("CREATE INDEX coins_history_symbol_idx ON coins_history (symbol)", "DROP INDEX coins_history_symbol_idx")
]
