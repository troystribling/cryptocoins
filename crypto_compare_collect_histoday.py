from time import sleep
from datetime import datetime

from cryptocoins.crypto_compare.requests import request_coin_price_history
from cryptocoins.crypto_compare.requests import coin_price_history_url
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory

max_coins = 2
max_pairs = 2
max_exchanges = 2

bucket_name = 'gly.fish'

# collect history
start_date = datetime.now()
print(f"INITIALIZE histoday {start_date}")

for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        print(f"REQUESTING histoday for CCCAGG, {currency_pair.from_symbol}, {currency_pair.to_symbol}")
        request_coin_price_history(currency_pair.from_symbol, currency_pair.to_symbol, allData='true')
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            print(f"REQUESTING histoday for {exchange.name}, {exchange.from_symbol}, {exchange.to_symbol}")
            request_coin_price_history(exchange.from_symbol, exchange.to_symbol, exchange=exchange.name, allData='true')
            sleep(2.0)

end_date = datetime.now()
print(f"COMPLETED histoday {end_date}")

import_coin_price_history(bucket_name, start_date, end_date)
