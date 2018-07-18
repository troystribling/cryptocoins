from time import sleep, time
from datetime import datetime

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.crypto_compare.requests import request_coin_list
from cryptocoins.crypto_compare.requests import request_top_currency_pairs
from cryptocoins.crypto_compare.requests import request_coin_snapshot

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.crypto_compare.imports import import_currency_pairs_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory

from cryptocoins.utils import setup_logging

bucket_name = sys.argv[1] if len(sys.argv) > 1 else 'gly.fish.data'
max_coins = sys.argv[2] if len(sys.argv) > 2 else 300
max_pairs = sys.argv[3] if len(sys.argv) > 3 else 300
max_exchanges = sys.argv[4] if len(sys.argv) > 4 else 100
log_out = sys.argv[5] if len(sys.argv) > 5 else '/var/log/apps/cryptocoins/crypto_compare_daily.log'

if log_out == 'stdout':
    logger = setup_logging()
else:
    logger = setup_logging(file_name=log_out)

logger.info(f"EXPORTING TO: {bucket_name}")
logger.info(f"COLLECTING DATA FOR {max_coins} coins, {max_pairs} curremcy_pairs AND {max_exchanges} exchanges")

timestamp_epoc = time()
logger.info(f"TIMESTAMP: {timestamp_epoc}")

# coins
start_date = datetime.utcnow()
logger.info(f"INITIALIZE coins: {start_date}")

request_coin_list(bucket_name, timestamp_epoc)

end_date = datetime.utcnow()
logger.info(f"COMPLETED coins {end_date}")

import_coin_list(bucket_name, start_date, end_date)
sleep(2.0)


# currency_pairs_history
start_date = datetime.utcnow()
logger.info(f"INITIALIZE currency_pairs_history {start_date}")

for coin in Coins.top_coins(limit=max_coins):
    logger.info(f"FETCHING currency pairs for {coin.symbol}")
    request_top_currency_pairs(bucket_name, coin.symbol, timestamp_epoc, limit=max_pairs)
    sleep(2.0)

end_date = datetime.utcnow()
logger.info(f"COMPLETED currency_pairs_history {end_date}")

import_currency_pairs_history(bucket_name, start_date, end_date)


# coins_history and exchanges_history
start_date = datetime.utcnow()
logger.info(f"INITIALIZE coins_history and exchanges_history {start_date}")

for coin in Coins.top_coins(limit=max_pairs):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        logger.info(f"FETCHING coin_snap_shot for currency pair {currency_pair.from_symbol}, {currency_pair.to_symbol}")
        request_coin_snapshot(bucket_name, currency_pair.from_symbol, currency_pair.to_symbol, timestamp_epoc)
        sleep(2.0)

end_date = datetime.utcnow()
logger.info(f"COMPLETED coins_history and exchanges_history {end_date}")

import_coin_snapshot(bucket_name, start_date, end_date)
