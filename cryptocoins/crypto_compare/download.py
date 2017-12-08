from cryptocoins.import_data import import_from_s3

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory

bucket_name = 'gly.fish'

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")


@download_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def download_coin_snapshot(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
        return
    coin_snapshot = data[0]
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot)


@download_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_list')
def download_coin_list(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    if 'Data' not in data[0]:
        print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
        return
    for coin in data[0]['Data'].values():
        Coins.create_or_update_using_crytocompare_coinlist(coin)


@download_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/top_pairs')
def download_currency_pairs_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    top_pairs = data[0]
    CurrencyPairsHistory.create_from_top_pairs(top_pairs)


@download_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/histoday')
def download_coin_price_history(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    histoday = data[0]
    CoinsPriceHistory.create_from_histoday(histoday, batch_size=1000)
