"""
CREATE coins table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coins"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " algorithm TEXT,"
         " coin_name TEXT,"
         " full_name TEXT,"
         " fully_premined BOOLEAN,"
         " coincompare_id BIGINT,"
         " name TEXT,"
         " proof_type TEXT,"
         " symbol TEXT,"
         " total_coin_supply BIGINT,"
         " PRIMARY KEY (id)"
         ")", "DROP TABLE COINS"),
    step("CREATE UNIQUE INDEX symbol_idx ON films (symbol)", "DROP INDEX symbol_idx")
]
