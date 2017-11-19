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
         " from_symbol TEXT,"
         " to_symbol TEXT,"
         " volume24h NUMERIC(21, 21),"
         " volume24hTo NUMERIC(21, 21)"
         ")", "DROP TABLE currency_pairs_history"),
    step("CREATE INDEX currency_pairs_history_from_to_symbol_idx ON currency_pairs_history (from_symbol, to_symbol)", "DROP INDEX currency_pairs_history_from_to_symbol_idx"),
    step("CREATE INDEX currency_pairs_history_from_symbol_idx ON currency_pairs_history (from_symbol)", "DROP INDEX currency_pairs_history_from_symbol_idx"),
    step("CREATE INDEX currency_pairs_history_to_symbol_idx ON currency_pairs_history (to_symbol)", "DROP INDEX currency_pairs_history_to_symbol_idx")
]
