from datetime import datetime
from time import sleep

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.one_forge.imports import import_exchange_rates
from cryptocoins.one_forge.requests import request_exchange_rate
from cryptocoins.utils import setup_logging

from_symbol = sys.argv[1] if len(sys.argv) > 1 else 'USD'
bucket_name = sys.argv[2] if len(sys.argv) > 2 else 'gly.fish.data'
log_out = sys.argv[3] if len(sys.argv) > 3 else '/var/log/apps/cryptocoins/one_forge_daily.log'

to_symbols = ['XAU', 'XAG']
collection_start = datetime.utcnow()

if log_out == 'stdout':
    logger = setup_logging()
else:
    logger = setup_logging(file_name=log_out)

api_key_file = os.path.join(os.environ["HOME"], '.one_forge', 'apikey')
api_key = open(api_key_file, 'r').read()

if __name__ == '__main__':
    logger.info(f"EXPORTING TO: {bucket_name}")
    logger.info(f"COLLECTING DATA FOR {collection_start.strftime('%Y%m%d')} AND FROM_SYMBOL '{from_symbol}'")
    for to_symbol in to_symbols:
        request_exchange_rate(bucket_name, api_key, from_symbol, to_symbol)
        sleep(10)
    import_exchange_rates(bucket_name, collection_start, collection_start)
