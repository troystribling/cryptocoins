from peewee import Model, PostgresqlDatabase, InternalError, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging
import pandas

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
        logger.info(f"DATA: {data}")

    @classmethod
    def create_from_fixer_exchange_rate(cls, data):
        logger.info(f"DATA: {data}")
