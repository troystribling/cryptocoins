"""
CREATE coin_list table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coin_list"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " algorithm TEXT,"
         " coin_name TEXT,"
         " full_name TEXT,"
         " fully_premined BOOLEAN,"
         " coin_id BIGINT,"
         " name TEXT,"
         " premined_value BIGINT,"
         " proof_type TEXT,"
         " sort_order BIGINT,"
         " sponsored BOOLEAN,"
         " symbol TEXT,"
         " total_coin_supply BIGINT,"
         " total_coins_free_float BIGINT,"
         " image_url TEXT,"
         " url TEXT,"
         " PRIMARY KEY (id)"
         ")")
]
