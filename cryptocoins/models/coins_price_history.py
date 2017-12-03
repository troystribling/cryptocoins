from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

from cryptocoins.utils import valid_params

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CoinsPriceHistory(BaseModel):
    close_price_24_hour = DecimalField()
    created_at = DateTimeField()
    exchange = TextField()
    from_symbol = TextField(index=True)
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    open_price_24_hour = DecimalField()
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    to_symbol = TextField(index=True)
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'coins_price_history'
        indexes = (
            (('from_symbol', 'to_symbol', 'timestamp'), True),
        )

    @classmethod
    def create_from_histoday(cls, histoday, batch_size=1000):
        expected_keys = ['CurrencyFrom', 'CurrencyTo', 'Exchange', 'Data']
        if not valid_params(expected_params=expected_keys, params=histoday):
            raise ValueError('ERROR: histoday keys invalid')

        records = histoday['Data']
        from_symbol = histoday['CurrencyFrom']
        to_symbol = histoday['CurrencyTo']
        exchange = histoday['Exchange']

        with database.atomic():
            for i in range(0, len(records), batch_size):
                model_params = [cls.histoday_to_model_parameters(record, from_symbol, to_symbol, exchange) for record in records[i:i + batch_size]]
                cls.insert_many(model_params).execute()

    @classmethod
    def histoday_to_model_parameters(cls, histoday, from_symbol, to_symbol, exchange):
        expected_keys = ['time', 'close', 'high', 'low', 'open', 'volumefrom', 'volumeto']
        if not valid_params(expected_params=expected_keys, params=histoday):
            raise ValueError('ERROR: histoday keys invalid')
        timestamp_epoc = histoday['time']
        return {'close_price_24_hour': histoday['close'],
                'exchange': exchange,
                'from_symbol': from_symbol,
                'high_price_24_hour': histoday['high'],
                'low_price_24_hour': histoday['low'],
                'open_price_24_hour': histoday['open'],
                'timestamp': datetime.fromtimestamp(int(timestamp_epoc)),
                'timestamp_epoc': timestamp_epoc,
                'to_symbol': to_symbol,
                'volume_from_24_hour': histoday['volumefrom'],
                'volume_to_24_hour': histoday['volumeto']}
