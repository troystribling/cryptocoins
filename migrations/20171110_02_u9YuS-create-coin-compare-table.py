"""
CREATE coin_snapshot table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE coin_snapshot"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " PRIMARY KEY (id)"
         ")")
]
