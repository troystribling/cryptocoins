"""
CREATE exchanges table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE exchanges"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " PRIMARY KEY (id)"
         ")")
]
