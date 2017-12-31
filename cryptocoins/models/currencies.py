from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime
import logging
import pandas

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Currencies(BaseModel):
    created_at = DateTimeField()
    name = TextField(null=True)
    symbol = TextField(index=True)
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    volume_total = DecimalField()
    volume_total_btc = DecimalField()
    volume_total_usd = DecimalField()

    class Meta:
        db_table = 'currencies'
        indexes = (
            (('symbol', 'timestamp_epoc'), True),
        )
