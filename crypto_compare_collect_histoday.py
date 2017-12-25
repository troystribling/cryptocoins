from time import sleep
from datetime import datetime

from cryptocoins.crypto_compare.requests import request_coin_price_history
from cryptocoins.crypto_compare.requests import coin_price_history_url
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.collections import Collections

from cryptocoins.utils import log

max_coins = 2
max_pairs = 2
max_exchanges = 2

bucket_name = 'gly.fish'

# collect history
start_date = datetime.utcnow()
log(f"INITIALIZE histoday {start_date}")


def request(exchange, from_symbol, to_symbol):
    meta = f"{exchange}/{from_symbol}/{to_symbol}"
    path = 'cryptocoins/cryptocompare/histoday'
    (last_collection_date) = Collections.lastest_collection_for_path_and_meta(path, meta)
    if last_collection_date is None:
        log(f"REQUESTING ALL histoday for {exchange}, {from_symbol}, {to_symbol}")
        request_coin_price_history(from_symbol, to_symbol, exchange=exchange, allData='true')
        return
    time_delta = datetime.utcnow() - last_collection_date
    limit = time_delta.days - 1
    if limit > 0:
        log(f"REQUESTING histoday for  {time_delta.days} days ago, {exchange}, {from_symbol}, {to_symbol}")
        request_coin_price_history(from_symbol, to_symbol, limit=limit, exchange=exchange, allData='false')
    else:
        print(f"COLLECT LIMIT < 0 SKIPPING COLLECTION {time_delta.days} DAYS AGO FOR, {exchange}, {from_symbol}, {to_symbol}")
    return


for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        request('CCCAGG', currency_pair.from_symbol, currency_pair.to_symbol)
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            request(exchange.name, exchange.from_symbol, exchange.to_symbol)
            sleep(2.0)

end_date = datetime.utcnow()
log(f"COMPLETED histoday {end_date}")

import_coin_price_history(bucket_name, start_date, end_date)
