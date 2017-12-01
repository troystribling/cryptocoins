# %%
from dateutil.parser import parse

from cryptocoins.import_data import import_from_s3

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory


bucket_name = 'gly.fish'
start_date = parse('20171125')
end_date = parse('20171125')


# %%
# coin_list
@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    for coin in data[0]['Data'].values():
        Coins.create_or_update_using_crytocompare_coinlist(coin)


import_coin_list()


# %%
# coin_snapshot
@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    coin_snapshot = data[0]['Data']
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot)


import_coin_snapshot()


# %%
# top_currency_pairs
@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/top_pairs')
def import_currency_pairs_history(data):
    top_pairs = data[0]['Data']
    print(top_pairs)
    CurrencyPairsHistory.create_from_top_pairs(top_pairs)


import_currency_pairs_history()


# %%
# coin_price_history
@import_from_s3(bucket_name=bucket_name, start_date=start_date, end_date=end_date, remote_dir='cryptocoins/cryptocompare/histoday')
def import_coin_price_history(data):
    histoday = data[0]['Data']
    CoinsPriceHistory.create_from_histoday(histoday)


import_coin_price_history()
