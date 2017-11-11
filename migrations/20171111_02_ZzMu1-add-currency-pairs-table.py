"""
Add currency pairs table
"""

from yoyo import step

__depends__ = {'20171111_01_ryOd4-add-import-table'}

steps = [
    step("CREATE TABLE currency_pairs"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " from_symbol TEXT,"
         " to_symbol TEXT,"
         " PRIMARY KEY (id)"
         ")", "DROP TABLE currency_pairs"),
    step("CREATE UNIQUE INDEX from_to_symbol_idx ON films (from_symbol, to_symbol)", "DROP INDEX from_to_symbol_idx")
]
