"""
CREATE currency_pairs_history table
"""

from yoyo import step

__depends__ = {

}

steps = [
    step("CREATE TABLE currency_pairs_history"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT NOT NULL,"
         " to_symbol TEXT NOT NULL,"
         " exchange TEXT NOT NULL,"
         " volume_from_24_hour NUMERIC(36, 21) NOT NULL DEFAULT 0.0,"
         " volume_to_24_hour NUMERIC(36, 21) NOT NULL DEFAULT 0.0"
         ")", "DROP TABLE currency_pairs_history"),
    step("CREATE INDEX currency_pairs_history_from_to_symbol_idx ON currency_pairs_history (from_symbol, to_symbol)", "DROP INDEX currency_pairs_history_from_to_symbol_idx"),
    step("CREATE INDEX currency_pairs_history_from_symbol_idx ON currency_pairs_history (from_symbol)", "DROP INDEX currency_pairs_history_from_symbol_idx"),
    step("CREATE INDEX currency_pairs_history_to_symbol_idx ON currency_pairs_history (to_symbol)", "DROP INDEX currency_pairs_history_to_symbol_idx")
]
