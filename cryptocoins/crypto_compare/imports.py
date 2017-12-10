from cryptocoins.import_data import import_from_s3

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory

bucket_name = 'gly.fish'


@import_from_s3(bucket_name=bucket_name, remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
        return
    coin_snapshot = data[0]
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot)


@import_from_s3(bucket_name=bucket_name, remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    if 'Data' not in data[0]:
        print(f"ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full: {data[0]}")
        return
    for coin in data[0]['Data'].values():
        Coins.create_or_update_using_crytocompare_coinlist(coin)


@import_from_s3(bucket_name=bucket_name, remote_dir='cryptocoins/cryptocompare/top_pairs')
def import_currency_pairs_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    top_pairs = data[0]
    CurrencyPairsHistory.create_from_top_pairs(top_pairs)


@import_from_s3(bucket_name=bucket_name, remote_dir='cryptocoins/cryptocompare/histoday')
def import_coin_price_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    histoday = data[0]
    CoinsPriceHistory.create_from_histoday(histoday, batch_size=1000)
