from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class ExchangesHistory(BaseModel):
    close_price_24_hour = DecimalField()
    created_at = DateTimeField()
    from_symbol = TextField()
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    name = TextField(index=True)
    open_price_24_hour = DecimalField()
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    to_symbol = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'exchanges_history'
