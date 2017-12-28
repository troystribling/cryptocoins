from time import sleep
from datetime import datetime


from cryptocoins.crypto_compare.requests import request_coin_list
from cryptocoins.crypto_compare.requests import request_top_currency_pairs
from cryptocoins.crypto_compare.requests import request_coin_snapshot

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.crypto_compare.imports import import_currency_pairs_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory

from cryptocoins.utils import setup_logging

logger = setup_logging(file_name= '/var/log/apps/cryptocoins/crypto_compare_daily.log')

max_coins = 2
max_pairs = 2
max_exchanges = 2

bucket_name = 'gly.fish'

# coins
start_date = datetime.utcnow()
logger.info(f"INITIALIZE coins with start date: {start_date}")

request_coin_list()

end_date = datetime.utcnow()
logger.info(f"COMPLETED coins {end_date}")

import_coin_list(bucket_name, start_date, end_date)
sleep(2.0)


# currency_pairs_history
start_date = datetime.utcnow()
logger.info(f"INITIALIZE currency_pairs_history {start_date}")

for coin in Coins.top_coins(limit=max_coins):
    logger.info(f"FETCHING currency pairs for {coin.symbol}")
    request_top_currency_pairs(coin.symbol, limit=max_pairs)
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
        request_coin_snapshot(currency_pair.from_symbol, currency_pair.to_symbol)
        sleep(2.0)

end_date = datetime.utcnow()
logger.info(f"COMPLETED coins_history and exchanges_history {end_date}")

import_coin_snapshot(bucket_name, start_date, end_date)
