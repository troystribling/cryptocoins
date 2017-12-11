import sys
from time import sleep
from datetime import date
from dateutil.parser import parse

from cryptocoins.utils import day_dir

from cryptocoins.crypto_compare.requests import request_coin_price_history
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory

import_date = date.today()
print(f"INITALIZING {day_dir(import_date)}")

max_coins = parse(sys.argv[1]) if len(sys.argv) > 1 else 100
max_pairs = parse(sys.argv[2]) if len(sys.argv) > 2 else 50
max_exchanges = parse(sys.argv[3]) if len(sys.argv) > 3 else 50

for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        print(f"REQUESTING HISTODAY for CCCAGG, {currency_pair.from_symbol}, {currency_pair.to_symbol}")
        request_coin_price_history(currency_pair.from_symbol, currency_pair.to_symbol, allData='true')
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            print(f"REQUESTING HISTODAY for {exchange.name}, {exchange.from_symbol}, {exchange.to_symbol}")
            request_coin_price_history(currency_pair.from_symbol, currency_pair.to_symbol, exchange=exchange.name, allData='true')
            sleep(2.0)

import_coin_price_history(import_date, import_date)
