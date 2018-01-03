from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime
import logging
import pandas
import time

logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Currencies(BaseModel):
    created_at = DateTimeField()
    name = TextField(null=True)
    symbol = TextField(index=True)
    timestamp_epoc = DecimalField()
    volume_total = DecimalField()
    volume_total_btc = DecimalField()
    volume_total_usd = DecimalField()
    price_usd = DecimalField()
    price_btc = DecimalField()

    class Meta:
        db_table = 'currencies'
        indexes = (
            (('symbol', 'timestamp_epoc'), True),
        )

    @classmethod
    def latest_for_symbol(cls, symbol):
        return cls.raw("SELECT * FROM currencies WHERE symbol = %s ORDER BY timestamp_epoc DESC LIMIT 1")

    @classmethod
    def create_for_symbols(cls, symbols, batch_size=100):
        if symbols is None:
            logger.error("symbols IS None")
            return
        timestamp_epoc = time.time()
        for i in range(0, len(symbols), batch_size):
            model_params = [cls.symbols_to_model_params(symbol, timestamp_epoc) for symbol in symbols[i:i + batch_size]]
            try:
                cls.insert_many(model_params).execute()
            except (IntegrityError, DataError) as error:
                logger.error(f"DATABASE ERROR for Currencies: {error}")
                continue

        @classmethod
        def symbols_to_model_params(cls, symbol, timestamp_epc):
            return {'symbol': symbol,
                    'timestamp_epoc': timestamp_epoc}
