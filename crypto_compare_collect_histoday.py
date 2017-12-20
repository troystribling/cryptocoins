from time import sleep
from datetime import datetime

from cryptocoins.crypto_compare.requests import request_coin_price_history
from cryptocoins.crypto_compare.requests import coin_price_history_url
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.collections import Collections

max_coins = 2
max_pairs = 2
max_exchanges = 2

bucket_name = 'gly.fish'

# collect history
start_date = datetime.now()
print(f"INITIALIZE histoday {start_date}")


def request(exchange, from_symbol, to_symbol):
    first_url = coin_price_history_url(from_symbol, to_symbol, exchange=exchange, allData='true')
    (first_collection_date) = Collections.lastest_collection_for(first_url)
    if first_collection_date is None:
        print(f"REQUESTING ALL histoday for  {datetime.now()}, {exchange}, {from_symbol}, {to_symbol}")
        request_coin_price_history(from_symbol, to_symbol, exchange=exchange, allData='true')
        return
    last_url = coin_price_history_url(from_symbol, to_symbol, exchange=exchange)
    (last_collection_date) = Collections.lastest_collection_for(last_url)
    if last_collection_date is None:
        print(f"REQUESTING FIRST histoday for  {datetime.now()}, {name}, {from_symbol}, {to_symbol}")
        return
    print(f"REQUESTING histoday for  {datetime.now()}, {name}, {from_symbol}, {to_symbol}")
    return


for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        request('CCCAGG', currency_pair.from_symbol, currency_pair.to_symbol)
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            request(exchange.name, exchange.from_symbol, exchange.to_symbol)
            sleep(2.0)

end_date = datetime.now()
print(f"COMPLETED histoday {end_date}")

import_coin_price_history(bucket_name, start_date, end_date)
