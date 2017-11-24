from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField


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
