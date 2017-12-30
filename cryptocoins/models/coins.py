from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime
import logging

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
    rank = BigIntegerField()
    symbol = TextField(unique=True)
    updated_at = DateTimeField()
    volume_total_usd = DecimalField()

    class Meta:
        db_table = 'coins'

    @classmethod
    def create_or_update_using_crytocompare_coinlist(cls, coin_list):
        expected_keys = ['CoinName', 'Id', 'FullName', 'Name', 'Symbol', 'SortOrder']
        if not valid_params(expected_params=expected_keys, params=coin_list):
            return

        try:
            with database.atomic():
                cls.create(coin_name=coin_list['CoinName'],
                           cryptocompare_id=coin_list['Id'],
                           full_name=coin_list['FullName'],
                           name=coin_list['Name'],
                           symbol=coin_list['Symbol'],
                           rank=coin_list['SortOrder'])
        except IntegrityError:
            query = cls.update(updated_at=datetime.utcnow(),
                               rank=coin_list['SortOrder']).where(Coins.symbol == coin_list['Symbol'])
            query.execute()
        except DataError as error:
            logger.error(f"DATABASE ERROR for Coin: {error}: {coin_list}")
            return None

    @classmethod
    def top_coins(cls, limit=None):
        if limit is None:
            return cls.raw("SELECT symbol FROM coins ORDER BY rank")
        else:
            return cls.raw("SELECT symbol FROM coins ORDER BY rank ASC LIMIT %s", limit)

    @classmethod
    def top_coins_data_frame(cls, limit=None):
        coins = [coin for coin in cls.top_coins(limit=limit).dicts()]
        index = [coin['id'] for coin in coins]
        return pandas.DataFrame(coins, index=index)
