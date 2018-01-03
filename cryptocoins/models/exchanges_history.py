from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging

from cryptocoins.utils import valid_params


logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


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
    timestamp_epoc = DecimalField()
    last_update_epoc = BigIntegerField()
    to_symbol = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'exchanges_history'

    @classmethod
    def create_from_coin_snapshot(cls, data, batch_size=100):
        expected_keys = ['timestamp_epoc', 'Data']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error('coin_snapshot KEYS INVALID')
            return

        coin_snapshot = data['Data']
        timestamp_epoc = data['timestamp_epoc']

        if 'Exchanges' not in coin_snapshot:
            logger.error(f"Exchanges KEY IS MISSING FROM coin_snapshot: {coin_snapshot}")
            return
        exchanges = coin_snapshot['Exchanges']

        with database.atomic():
            for i in range(0, len(exchanges), batch_size):
                model_params = [cls.exchange_to_model_params(exchange, timestamp_epoc) for exchange in exchanges[i:i + batch_size]]
                try:
                    cls.insert_many(model_params).execute()
                except (IntegrityError, DataError, ValueError) as error:
                    logger.error(f"DATABASE ERROR for ExchangesHistory: {error}")
                    continue

    @classmethod
    def exchange_to_model_params(cls, exchange, timestamp_epoc):
        expected_keys = ['FROMSYMBOL', 'HIGH24HOUR', 'LOW24HOUR', 'LASTUPDATE', 'MARKET',
                         'OPEN24HOUR', 'TOSYMBOL', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=exchange):
            raise ValueError('Exchange keys invalid')
        last_update_epoc = exchange['LASTUPDATE']
        return {'from_symbol': exchange['FROMSYMBOL'],
                'high_price_24_hour': exchange['HIGH24HOUR'],
                'low_price_24_hour': exchange['LOW24HOUR'],
                'name': exchange['MARKET'],
                'open_price_24_hour': exchange['OPEN24HOUR'],
                'close_price_24_hour': exchange['PRICE'],
                'timestamp_epoc': timestamp_epoc,
                'last_update_epoc': last_update_epoc,
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
