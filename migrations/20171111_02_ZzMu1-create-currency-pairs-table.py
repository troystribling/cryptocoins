"""
CREATE currency pairs table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE currency_pairs"
         "("
         " id SERIAL PRIMARY KEY, "
         " created_at TIMESTAMP NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),"
         " from_symbol TEXT,"
         " to_symbol TEXT,"
         " cryptocompare_subscription TEXT"
         ")", "DROP TABLE currency_pairs"),
    step("CREATE UNIQUE INDEX currency_pairs_from_to_symbol_idx ON currency_pairs (from_symbol, to_symbol)", "DROP INDEX currency_pairs_from_to_symbol_idx"),
    step("CREATE INDEX currency_pairs_from_symbol_idx ON currency_pairs (from_symbol)", "DROP INDEX currency_pairs_from_symbol_idx"),
    step("CREATE INDEX currency_pairs_to_symbol_idx ON currency_pairs (to_symbol)", "DROP INDEX currency_pairs_to_symbol_idx")
]
