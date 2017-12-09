
from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

from cryptocoins.utils import valid_params


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


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

    @classmethod
    def top_coins(cls, limit=100):
        return cls.raw("SELECT symbol FROM coins ORDER BY rank ASC LIMIT %s", limit)
