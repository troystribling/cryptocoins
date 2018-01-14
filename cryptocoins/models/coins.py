from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging
import pandas

from cryptocoins.utils import valid_params

logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = database


class Coins(BaseModel):
    coin_name = TextField()
    created_at = DateTimeField()
    cryptocompare_id = BigIntegerField()
    full_name = TextField()
    name = TextField()
    crypto_compare_rank = BigIntegerField()
    symbol = TextField(unique=True)
    volume_total_usd = DecimalField()
    volume_total_btc = DecimalField()
    volume_total = DecimalField()
    price_usd = DecimalField()
    price_btc = DecimalField()
    spread_usd = DecimalField()
    spread_btc = DecimalField()
    marketcap_usd = DecimalField()
    marketcap_btc = DecimalField()
    timestamp_epoc = DecimalField()

    class Meta:
        db_table = 'coins'

    @classmethod
    def create_from_crytocompare_coinlist(cls, data, batch_size=100):
        expected_keys = ['timestamp_epoc', 'Data']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error('coinlist KEYS INVALID')
            return
        coins = [coin for coin in data['Data'].values()]
        timestamp_epoc = data['timestamp_epoc']
        for i in range(0, len(coins), batch_size):
            model_params = [cls.coin_list_to_model_params(coin, timestamp_epoc) for coin in coins[i:i + batch_size]]
            try:
                cls.insert_many(model_params).execute()
            except (IntegrityError, DataError, ValueError) as error:
                logger.error(f"DATABASE ERROR for Coins: {error}")
                continue

    @classmethod
    def coin_list_to_model_params(cls, coin_list, timestamp_epoc):
        expected_keys = ['CoinName', 'Id', 'FullName', 'Name', 'Symbol', 'SortOrder']
        if not valid_params(expected_params=expected_keys, params=coin_list):
            raise ValueError('Coin List keys invalid')
        return {'coin_name': coin_list['CoinName'],
                'cryptocompare_id': coin_list['Id'],
                'full_name': coin_list['FullName'],
                'name': coin_list['Name'],
                'symbol': coin_list['Symbol'],
                'crypto_compare_rank': coin_list['SortOrder'],
                'timestamp_epoc': timestamp_epoc}

    @classmethod
    def top_coins(cls, limit=None):
        if limit is None:
            return cls.raw("SELECT * FROM coins WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM coins) ORDER BY crypto_compare_rank")
        else:
            return cls.raw("SELECT * FROM coins"
                           " WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM coins) ORDER BY crypto_compare_rank LIMIT %s", limit)

    @classmethod
    def top_coins_data_frame(cls, limit=None):
        records = [record for record in cls.top_coins(limit=limit).dicts()]
        index = [record['id'] for record in records]
        return pandas.DataFrame(records, index=index)
