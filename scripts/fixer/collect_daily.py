from datetime import datetime

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.fixer.imports import import_exchange_rates
from cryptocoins.fixer.requests import request_latest_exchange_rate
from cryptocoins.utils import setup_logging

from_symbol = sys.argv[1] if len(sys.argv) > 1 else 'USD'
bucket_name = sys.argv[2] if len(sys.argv) > 2 else 'gly.fish'
log_out = sys.argv[3] if len(sys.argv) > 3 else '/var/log/apps/cryptocoins/fixer_daily.log'

collection_start = datetime.utcnow()

if log_out == 'stdout':
    logger = setup_logging()
else:
    logger = setup_logging(file_name=log_out)

if __name__ == '__main__':
    if collection_start.weekday() < 5:
        logger.info(f"EXPORTING TO: {bucket_name}")
        logger.info(f"COLLECTING DATA FOR {collection_start.strftime('%Y%m%d')} AND FROM_SYMBOL '{from_symbol}'")
        request_latest_exchange_rate(bucket_name, from_symbol)
        import_exchange_rates(bucket_name, collection_start, collection_start)
    else:
        logger.info(f"SKIPPINMG COLLECTION SINCE DAY IS WEEKEND")
