import sys
from datetime import date

from dateutil.parser import parse

from cryptocoins.import_data import import_from_s3

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory

start_date = parse(sys.argv[1]) if len(sys.argv) else date.today()
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date

bucket_name = 'gly.fish'

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
        return
    coin_snapshot = data[0]
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot)


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    if 'Data' not in data[0]:
        print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
        return
    for coin in data[0]['Data'].values():
        Coins.create_or_update_using_crytocompare_coinlist(coin)


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/top_pairs')
def import_currency_pairs_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    top_pairs = data[0]
    CurrencyPairsHistory.create_from_top_pairs(top_pairs)


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/histoday')
def import_coin_price_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    histoday = data[0]
    CoinsPriceHistory.create_from_histoday(histoday)


import_coin_snapshot()
import_coin_list()
import_currency_pairs_history()
import_coin_price_history()
