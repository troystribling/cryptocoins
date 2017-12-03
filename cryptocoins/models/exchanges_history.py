from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

from cryptocoins.utils import valid_params

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class ExchangesHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField()
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    name = TextField(index=True)
    open_price_24_hour = DecimalField()
    close_price_24_hour = DecimalField()
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    to_symbol = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'exchanges_history'

    @classmethod
    def create_from_coin_snapshot(cls, data, batch_size=100):
        if 'Data' not in data:
            print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot")
            return

        coin_snapshot = data['Data']

        exchanges = coin_snapshot['Exchanges']
        if 'Exchanges' not in coin_snapshot:
            print("ERROR: Exchanges KEY IS MISSING FROM import_coin_snapshot")
            return

        with database.atomic():
            for i in range(0, len(exchanges), batch_size):
                model_params = [cls.exchange_to_model_params(exchange) for exchange in exchanges[i:i + batch_size]]
                cls.insert_many(model_params).execute()

    @classmethod
    def exchange_to_model_params(cls, exchange):
        expected_keys = ['FROMSYMBOL', 'HIGH24HOUR', 'LOW24HOUR', 'LASTUPDATE', 'MARKET',
                         'OPEN24HOUR', 'TOSYMBOL', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=exchange):
            raise ValueError('ERROR: Exchange keys invalid')
        timestamp_epoc = exchange['LASTUPDATE']
        return {'from_symbol': exchange['FROMSYMBOL'],
                'high_price_24_hour': exchange['HIGH24HOUR'],
                'low_price_24_hour': exchange['LOW24HOUR'],
                'name': exchange['MARKET'],
                'open_price_24_hour': exchange['OPEN24HOUR'],
                'close_price_24_hour': exchange['PRICE'],
                'timestamp': datetime.fromtimestamp(int(timestamp_epoc)),
                'timestamp_epoc': timestamp_epoc,
                'to_symbol': exchange['TOSYMBOL'],
                'volume_from_24_hour': exchange['VOLUME24HOUR'],
                'volume_to_24_hour': exchange['VOLUME24HOURTO']}
