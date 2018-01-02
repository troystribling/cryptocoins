# %%
from dateutil.parser import parse
import logging

from cryptocoins.import_data import import_from_s3

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory

from cryptocoins.utils import setup_logging

bucket_name = 'gly.fish.dev'
logger = setup_logging()

# %%
# coin_list
start_date = parse('20171230')
end_date = parse('20180101')


@import_from_s3(remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    if 'Data' not in data[0]:
        logger.error(f"Data KEY IS MISSING FROM import_coin_snapshot_full: {data[0]}")
        return
    coin_list = [coin for coin in data[0]['Data'].values()]
    Coins.create_from_crytocompare_coinlist(coin_list, batch_size=10)


import_coin_list(bucket_name, start_date, end_date)


# %%
# currencies


# %%
# coin_snapshot, coin_history, exchanges_history
start_date = parse('20171230')
end_date = parse('20171230')


@import_from_s3(remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    coin_snapshot = data[0]
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot, batch_size=100)


import_coin_snapshot(bucket_name, start_date, end_date)


# %%
# top_currency_pairs
start_date = parse('20171230')
end_date = parse('20171230')


@import_from_s3(remote_dir='cryptocoins/cryptocompare/top_pairs')
def import_currency_pairs_history(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    top_pairs = data[0]
    CurrencyPairsHistory.create_from_top_pairs(top_pairs, batch_size=100)


import_currency_pairs_history(bucket_name, start_date, end_date)


# %%
# coin_price_history
start_date = parse('20171230')
end_date = parse('20171230')


@import_from_s3(remote_dir='cryptocoins/cryptocompare/histoday')
def import_coin_price_history(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    histoday = data[0]
    CoinsPriceHistory.create_from_histoday(histoday, batch_size=100)


import_coin_price_history(bucket_name, start_date, end_date)
