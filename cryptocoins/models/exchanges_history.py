from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
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
            print(f"ERROR: Data KEY IS MISSING FROM coin_snapshot: {data}")
            return
        coin_snapshot = data['Data']

        if 'Exchanges' not in coin_snapshot:
            print(f"ERROR: Exchanges KEY IS MISSING FROM coin_snapshot: {coin_snapshot}")
            return
        exchanges = coin_snapshot['Exchanges']

        with database.atomic():
            for i in range(0, len(exchanges), batch_size):
                model_params = [cls.exchange_to_model_params(exchange) for exchange in exchanges[i:i + batch_size]]
                try:
                    cls.insert_many(model_params).execute()
                except IntegrityError as error:
                    print(f"ERROR: Exchange History Update Exists: {error}")
                    continue
                except DataError as error:
                    print(f"ERROR: ExchangesHistory Precision failure for {exchanges}: {error}")
                    return None

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
                'timestamp': datetime.utcfromtimestamp(int(timestamp_epoc)),
                'timestamp_epoc': timestamp_epoc,
                'to_symbol': exchange['TOSYMBOL'],
                'volume_from_24_hour': exchange['VOLUME24HOUR'],
                'volume_to_24_hour': exchange['VOLUME24HOURTO']}

    @classmethod
    def top_exchanges_for_currency_pair(cls, from_symbol, to_symbol, limit=10):
            query = "SELECT full_table.created_at, full_table.name, full_table.from_symbol," \
                    " full_table.to_symbol, full_table.volume_from_24_hour" \
                    " FROM exchanges_history AS full_table" \
                    " INNER JOIN" \
                    " (SELECT MAX(id) AS latest_id, name, from_symbol, to_symbol FROM exchanges_history GROUP" \
                    " BY name, from_symbol, to_symbol HAVING from_symbol = %s AND to_symbol = %s)" \
                    " AS latest ON (full_table.id = latest.latest_id)" \
                    " ORDER BY full_table.volume_from_24_hour DESC LIMIT %s"
            return ExchangesHistory.raw(query, from_symbol, to_symbol, limit)
