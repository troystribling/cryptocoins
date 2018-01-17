from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging
import pandas

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
    def top_exchanges_for_currency_pair(cls, from_symbol, to_symbol, limit=None):
        if limit is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM exchanges_history)"
                           "  AND from_symbol = %s AND to_symbol = %s ORDER BY volume_from_24_hour DESC", from_symbol, to_symbol)
        else:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM exchanges_history)"
                           "  AND from_symbol = %s AND to_symbol = %s ORDER BY volume_from_24_hour DESC LIMIT %s", from_symbol, to_symbol, limit)

    @classmethod
    def top_exchanges_for_currency_pair_data_frame(cls, from_symbol, to_symbol, limit=None):
        records = [record for record in cls.top_exchanges_for_currency_pair(from_symbol, to_symbol, limit).dicts()]
        index = [record['id'] for record in records]
        return pandas.DataFrame(records, index=index)

    @classmethod
    def history(cls, from_symbol, to_symbol=None, exchange=None):
        if exchange is None and to_symbol is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE from_symbol = %s"
                           " ORDER BY timestamp_epoc", from_symbol)
        elif exchange is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE from_symbol = %s AND to_symbol = %s"
                           " ORDER BY timestamp_epoc", from_symbol, to_symbol)
        elif to_symbol is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE from_symbol = %s AND exchange = %s"
                           " ORDER BY timestamp_epoc", from_symbol, exchange)
        else:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE from_symbol = %s AND to_symbol = %s AND exchange = %s"
                           " ORDER BY timestamp_epoc", from_symbol, to_symbol, exchange)

    @classmethod
    def history_data_frame(cls, from_symbol, to_symbol=None, exchange=None):
        records = [record for record in cls.history(from_symbol, to_symbol, exchange).dicts()]
        index = [record['last_update_epoc'] for record in records]
        return pandas.DataFrame(records, index=index)

    @classmethod
    def timestamps(cls):
        query = cls.raw("SELECT DISTINCT timestamp_epoc FROM exchanges_history ORDER BY timestamp_epoc DESC")
        return [timestamp.timestamp_epoc for timestamp in query]

    @classmethod
    def for_timestamp_epoc(cls, timestamp_epoc, from_symbol=None, to_symbol=None):
        if from_symbol is None and to_symbol is None:
            return cls.raw("SELECT * FROM exchanges_history WHERE timestamp_epoc = %s"
                           " ORDER BY from_symbol, volume_from_24_hour DESC", timestamp_epoc)
        elif from_symbol is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE timestamp_epoc = %s AND to_symbol = %s"
                           " ORDER BY from_symbol, volume_from_24_hour DESC", timestamp_epoc, to_symbol)
        elif to_symbol is None:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE timestamp_epoc = %s AND from_symbol = %s"
                           " ORDER BY from_symbol, volume_from_24_hour DESC", timestamp_epoc, from_symbol)
        else:
            return cls.raw("SELECT * FROM exchanges_history"
                           " WHERE timestamp_epoc = %s AND from_symbol = %s AND to_symbol = %s"
                           " ORDER BY from_symbol, volume_from_24_hour DESC", timestamp_epoc, from_symbol, to_symbol)

    @classmethod
    def for_timestamp_epoc_data_frame(cls, timestamp_epoc, from_symbol=None, to_symbol=None):
        records = [record for record in cls.for_timestamp_epoc(timestamp_epoc, from_symbol, to_symbol).dicts()]
        index = [record['name'] for record in records]
        return pandas.DataFrame(records, index=index)
