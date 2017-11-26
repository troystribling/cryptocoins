import sys
from datetime import date

from dateutil.parser import parse

from cryptocoins.import_data import import_from_s3
from cryptocoins.models.exchanges import Exchanges
from cryptocoins.models.currency_pairs import CurrencyPairs
from cryptocoins.models.coins import Coins

start_date = date.today()
if len(sys.argv) > 1:
    start_date = parse(sys.argv[1])

end_date = start_date
if len(sys.argv) > 2:
    end_date = parse(sys.argv[2])

bucket_name = 'gly.fish'

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
        return
    if 'Data' not in data[0]:
        print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
        return
    if 'Subs' not in data[0]['Data']:
        print("ERROR: Subs KEY IS MISSING FROM import_coin_snapshot_full")
        return
    coin_snapshot = data[0]['Data']
    CoinsHistory.create_using_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_using_coin_snapshot(coin_snapshot)


@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    if len(data) != 1:
        print("ERROR: FILE WRONG SIZE")
    if 'Data' not in data[0]:
        print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
        return
    for coin in data[0]['Data'].values():
        Coins.create_or_update_using_crytocompare_coinlist(coin)


import_coin_snapshot()
import_coin_list()
