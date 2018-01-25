from time import sleep
from dateutil.parser import parse
from datetime import datetime

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.fixer.imports import import_exchange_rates
from cryptocoins.fixer.requests import request_exchange_rate
import cryptocoins.utils as utils
from cryptocoins.utils import setup_logging

start_date = parse(sys.argv[1]) if len(sys.argv) > 1 else datetime.utcnow()
from_symbol = sys.argv[2] if len(sys.argv) > 2 else 'USD'
bucket_name = sys.argv[3] if len(sys.argv) > 3 else 'gly.fish'
end_date = datetime.utcnow()
collection_start = datetime.utcnow()

logger = setup_logging()

if __name__ == '__main__':
    logger.info(f"EXPORTING TO: {bucket_name}")
    logger.info(f"COLLECTING DATA FOR {start_date.strftime('%Y%m%d')} TO {end_date.strftime('%Y%m%d')} AND FROM_SYMBOL '{from_symbol}'")

    for day in utils.daterange(start_date, end_date):
        if day.weekday() < 5:
            logger.info(f"COLLECTING DATA FOR {day.strftime('%Y-%m-%d')} AND FROM_SYMBOL '{from_symbol}'")
            request_exchange_rate(bucket_name, day, from_symbol)
            sleep(10)

    collection_end = datetime.utcnow()
    import_exchange_rates(bucket_name, collection_start, collection_end)
