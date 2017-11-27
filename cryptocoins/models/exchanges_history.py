from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

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
    def create_from_coin_snapshot(cls, coin_snapshot, batch_size=100):
        exchanges = coin_snapshot['Exchanges']
        if 'Exchanges' not in coin_snapshot:
            print("ERROR: Exchanges KEY IS MISSING FROM import_coin_snapshot_full")
            return
        with database.atomic():
            for i in range(0, len(aggredated_data), batch_size):
                model_params = [cls.exchange_to_model_params(exchange) for exchange in exchanges[i:i*batch_size]]
                cls.insert_many(model_params).execute

    @classmethod
    def exchange_to_model_params(cls, exchanges):
        expected_keys = ['FROMSYMBOL', 'HIGH24HOUR', 'LOW24HOUR', 'LASTUPDATE', 'MARKET'
                         'OPEN24HOUR', 'TOSYMBOL', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=exchanges)
            raise ValueError('ERROR: Exchange keys invalid')
        timestamp_epoc = exchanges['LASTUPDATE']
        return {'from_symbol': exchanges['FROMSYMBOL'],
                'high_price_24_hour': exchanges['HIGH24HOUR'],
                'low_price_24_hour': exchanges['LOW24HOUR'],
                'name': exchanges['MARKET'],
                'open_price_24_hour': exchanges['OPEN24HOUR'],
                'close_price_24_hour': exchanges['PRICE']
                'timestamp': datetime.fromtimestamp(int(timestamp_epoc))),
                'timestamp_epoc': timestamp_epoc,
                'to_symbol': exchanges['TOSYMBOL'],
                'volume_from_24_hour': exchanges['VOLUME24HOUR'],
                'volume_to_24_hour': exchanges['VOLUME24HOURTO']}
