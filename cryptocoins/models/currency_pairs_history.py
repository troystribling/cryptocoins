from peewee import Model, PostgresqlDatabase, IntegrityError, InternalError, DataError, DateTimeField, TextField, DecimalField, BigIntegerField
from cryptocoins.utils import valid_params
import logging
import time


logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = database


class CurrencyPairsHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField(index=True)
    to_symbol = TextField(index=True)
    exchange = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()
    timestamp_epoc = BigIntegerField()

    class Meta:
        db_table = 'currency_pairs_history'
        indexes = (
            (('from_symbol', 'to_symbol'), False),
        )

    @classmethod
    def create_from_top_pairs(cls, data, batch_size=100):
        expected_keys = ['timestamp_epoc', 'Data']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error('coinlist KEYS INVALID')
            return

        top_pairs = data['Data']
        timestamp_epoc = data['timestamp_epoc']

        with database.atomic():
            for i in range(0, len(top_pairs), batch_size):
                model_params = [cls.top_pairs_to_model_params(top_pair, timestamp_epoc) for top_pair in top_pairs[i:i + batch_size]]
                try:
                    cls.insert_many(model_params).execute()
                except (IntegrityError, InternalError, DataError) as error:
                    logger.error(f"DATABASE ERROR FOR CurrencyPairsHistory: {error}")
                    continue

    @classmethod
    def top_pairs_to_model_params(cls, top_pair, timestamp_epoc):
        expected_keys = ['exchange', 'fromSymbol', 'toSymbol', 'volume24h', 'volume24hTo']
        if not valid_params(expected_params=expected_keys, params=top_pair):
            raise ValueError('ERROR: Top Pairs keys invalid')
        return {'from_symbol': top_pair['fromSymbol'],
                'to_symbol': top_pair['toSymbol'],
                'exchange': top_pair['exchange'],
                'timestamp_epoc': timestamp_epoc,
                'volume_from_24_hour': top_pair['volume24h'],
                'volume_to_24_hour': top_pair['volume24hTo']}

    @classmethod
    def currency_pairs_for_coin(cls, coin, limit=None):
        if limit is None:
            return cls.raw("SELECT full_table.created_at, full_table.exchange, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour"
                           " FROM currency_pairs_history AS full_table"
                           " JOIN"
                           "  (SELECT MAX(id) AS latest_id, exchange, from_symbol, to_symbol FROM currency_pairs_history"
                           "   GROUP BY exchange, from_symbol, to_symbol HAVING from_symbol = %s)"
                           "   AS latest ON (full_table.id = latest.latest_id)"
                           " ORDER BY full_table.volume_from_24_hour DESC", coin)
        else:
            return cls.raw("SELECT full_table.created_at, full_table.exchange, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour"
                           " FROM currency_pairs_history AS full_table"
                           " INNER JOIN"
                           "  (SELECT MAX(id) AS latest_id, exchange, from_symbol, to_symbol FROM currency_pairs_history"
                           "   GROUP BY exchange, from_symbol, to_symbol HAVING from_symbol = %s) AS latest"
                           " ON (full_table.id = latest.latest_id)"
                           " ORDER BY full_table.volume_from_24_hour DESC LIMIT %s", coin, limit)

    @classmethod
    def currencies(cls):
        symbols = cls.raw("SELECT to_symbol AS currency FROM"
                          " (SELECT coins.symbol, pairs.to_symbol FROM coins"
                          "  RIGHT JOIN"
                          "   (SELECT to_symbol FROM currency_pairs_history GROUP BY to_symbol) AS pairs"
                          "    ON coins.symbol = pairs.to_symbol WHERE coins.symbol IS NULL)"
                          " AS currencies").dicts()
        return [symbol['currency'] for symbol in symbols]
