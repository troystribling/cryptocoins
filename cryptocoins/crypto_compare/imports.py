from cryptocoins.import_data import import_from_s3
import logging

from cryptocoins.models.coins import Coins
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory


logger = logging.getLogger(__name__)


@import_from_s3(remote_dir='cryptocoins/cryptocompare/coin_list')
def import_coin_list(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    Coins.create_from_crytocompare_coinlist(data[0])


@import_from_s3(remote_dir='cryptocoins/cryptocompare/coin_snapshot')
def import_coin_snapshot(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    coin_snapshot = data[0]
    CoinsHistory.create_from_coin_snapshot(coin_snapshot)
    ExchangesHistory.create_from_coin_snapshot(coin_snapshot, batch_size=100)


@import_from_s3(remote_dir='cryptocoins/cryptocompare/top_pairs')
def import_currency_pairs_history(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    top_pairs = data[0]
    CurrencyPairsHistory.create_from_top_pairs(top_pairs, batch_size=100)


@import_from_s3(remote_dir='cryptocoins/cryptocompare/histoday')
def import_coin_price_history(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    histoday = data[0]
    CoinsPriceHistory.create_from_histoday(histoday, batch_size=100)
