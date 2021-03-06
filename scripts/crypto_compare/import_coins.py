from datetime import datetime
from dateutil.parser import parse

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.utils import setup_logging

logger = setup_logging()

start_date = parse(sys.argv[1]) if len(sys.argv) > 1 else datetime.utcnow()
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date
bucket_name = sys.argv[3] if len(sys.argv) > 3 else 'gly.fish'

logger.info(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")

if __name__ == "__main__":
    import_coin_list(bucket_name, start_date, end_date)
