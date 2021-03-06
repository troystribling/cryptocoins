from time import sleep
from datetime import datetime

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.crypto_compare.requests import request_coin_price_history
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.collections import Collections

from cryptocoins.utils import setup_logging

bucket_name = sys.argv[1] if len(sys.argv) > 1 else 'gly.fish.data'
max_coins = sys.argv[2] if len(sys.argv) > 2 else 300
max_pairs = sys.argv[3] if len(sys.argv) > 3 else 300
max_exchanges = sys.argv[4] if len(sys.argv) > 4 else 100

log_out = sys.argv[5] if len(sys.argv) > 5 else '/var/log/apps/cryptocoins/crypto_compare_histoday.log'

if log_out == 'stdout':
    logger = setup_logging()
else:
    logger = setup_logging(file_name=log_out)

logger.info(f"EXPORTING TO: {bucket_name}")
logger.info(f"COLLECTING DATA FOR {max_coins} coins, {max_pairs} curremcy_pairs AND {max_exchanges} exchanges")

# collect history
start_date = datetime.utcnow()
logger.info(f"INITIALIZE histoday {start_date}")


def request(exchange, from_symbol, to_symbol):
    meta = f"{exchange}/{from_symbol}/{to_symbol}"
    path = 'cryptocoins/cryptocompare/histoday'
    (last_collection_date) = Collections.lastest_collection_for_path_and_meta(path, meta)
    if last_collection_date is None:
        logger.info(f"REQUESTING ALL histoday for {exchange}, {from_symbol}, {to_symbol}")
        request_coin_price_history(bucket_name, from_symbol, to_symbol, exchange=exchange, allData='true')
        return
    time_delta = datetime.utcnow() - last_collection_date
    limit = time_delta.days - 1
    if limit > 0:
        logger.info(f"REQUESTING histoday for  {time_delta.days} days ago, {exchange}, {from_symbol}, {to_symbol}")
        request_coin_price_history(bucket_name, from_symbol, to_symbol, limit=limit, exchange=exchange, allData='false')
    else:
        logger.info(f"COLLECT LIMIT < 0 SKIPPING COLLECTION {time_delta.days} DAYS AGO FOR, {exchange}, {from_symbol}, {to_symbol}")
    return


for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        request('CCCAGG', currency_pair.from_symbol, currency_pair.to_symbol)
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            request(exchange.name, exchange.from_symbol, exchange.to_symbol)
            sleep(2.0)

end_date = datetime.utcnow()
logger.info(f"COMPLETED histoday {end_date}")

import_coin_price_history(bucket_name, start_date, end_date)
