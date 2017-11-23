from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CurrencyPairsHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField(index=True)
    to_symbol = TextField(index=True)
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'currency_pairs_history'
        indexes = (
            (('from_symbol', 'to_symbol'), False),
        )
