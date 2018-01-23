from peewee import Model, PostgresqlDatabase, InternalError, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging
from datetime import datetime
import pandas
from cryptocoins.utils import valid_params


logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})

class BaseModel(Model):
    class Meta:
        database = database

class ForexPairsHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField(index=True)
    price = DecimalField()
    timestamp_epoc = BigIntegerField()
    to_symbol = TextField()

    class Meta:
        db_table = 'forex_pairs_history'

    @classmethod
    def create_from_1forge_exchange_rate(cls, data):
        exchange_rate = cls.model_params_from_1forge_exchange_rate(data)
        if exchange_rate is None:
            return
        with database.atomic():
            try:
                cls.create(**exchange_rate)
            except (IntegrityError, DataError) as error:
                logger.error(f"DATABASE ERROR for ForexPairsHistory: {error}")

    @classmethod
    def model_params_from_1forge_exchange_rate(cls, data):
        expected_keys = ['value', 'timestamp', 'from_symbol', 'to_symbol']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error("1forge_exchange_rate KEYS INVALID")
            return None
        return {'from_symbol': data['from_symbol'],
                'to_symbol': data['to_symbol'],
                'price': data['value'],
                'timestamp_epoc': data['timestamp']}


    @classmethod
    def create_from_fixer_exchange_rate(cls, data, batch_size=100):
        params = cls.model_params_from_fixer_exchange_rate(data)
        if params is None:
            logger.error("fixer_exchange_rate KEYS INVALID")
            return
        with database.atomic():
            for i in range(0, len(params), batch_size):
                try:
                    cls.insert_many(params[i:i + batch_size]).execute()
                except (IntegrityError, InternalError, DataError) as error:
                    logger.error(f"DATABASE ERROR for ForexPairsHistory: {error}")
                    continue

    @classmethod
    def model_params_from_fixer_exchange_rate(cls, data):
        expected_keys = ['base', 'date', 'rates']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error("fixer_exchange_rate KEYS INVALID")
            return None
        timestamp_epoc = datetime.strptime(data['date'], '%Y-%m-%d').timestamp()
        from_symbol = data['base']
        params = []
        for to_symbol, rate in data['rates'].items():
            model_params = {'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'price': rate,
                            'timestamp_epoc': timestamp_epoc}
            params.append(model_params)
        return params
