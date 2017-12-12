from time import sleep
from datetime import date

from cryptocoins.utils import day_dir

from cryptocoins.crypto_compare.requests import request_coin_list
from cryptocoins.crypto_compare.requests import request_top_currency_pairs
from cryptocoins.crypto_compare.requests import request_coin_snapshot
from cryptocoins.crypto_compare.requests import request_coin_price_history

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.crypto_compare.imports import import_currency_pairs_history
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory

import_date = date.today()
print(f"INITALIZING {day_dir(import_date)}")

max_coins = 200
max_pairs = 100
max_exchanges = 100

# coins
print("INITIALIZE coins")
request_coin_list()
import_coin_list(import_date, import_date)
sleep(10.0)


# currency_pairs_history
print("INITIALIZE currency_pairs_history")
for coin in Coins.top_coins(limit=max_coins):
    print(f"FETCHING currency pairs for {coin.symbol}")
    request_top_currency_pairs(coin.symbol, limit=max_pairs)
    sleep(10.0)

import_currency_pairs_history(import_date, import_date)


# coins_history and exchanges_history
print("INITIALIZE coins_history and exchanges_history")
for coin in Coins.top_coins(limit=max_pairs):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        print(f"FETCHING coin_snap_shot for currency pair {currency_pair.from_symbol}, {currency_pair.to_symbol}")
        request_coin_snapshot(currency_pair.from_symbol, currency_pair.to_symbol)
        sleep(5.0)

import_coin_snapshot(import_date, import_date)

# collect history
for coin in Coins.top_coins(limit=max_coins):
    for currency_pair in CurrencyPairsHistory.currency_pairs_for_coin(coin.symbol, limit=max_pairs):
        print(f"REQUESTING HISTODAY for CCCAGG, {currency_pair.from_symbol}, {currency_pair.to_symbol}")
        request_coin_price_history(currency_pair.from_symbol, currency_pair.to_symbol, allData='true')
        sleep(2.0)
        for exchange in ExchangesHistory.top_exchanges_for_currency_pair(currency_pair.from_symbol, currency_pair.to_symbol, limit=max_exchanges):
            print(f"REQUESTING HISTODAY for {exchange.name}, {exchange.from_symbol}, {exchange.to_symbol}")
            request_coin_price_history(exchange.from_symbol, exchange.to_symbol, exchange=exchange.name, allData='true')
            sleep(2.0)

import_coin_price_history(import_date, import_date)
