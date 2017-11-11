"""
Add import table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE imports"
         "("
         " id BIGINT, "
         " created_at TIMESTAMP WITH TIME ZONE,"
         " import_type TEXT,"
         " file_type TEXT,"
         " start_date DATE,"
         " end_date DATE"
         " PRIMARY KEY (id)"
         ")", "DROP TABLE imports")
]
