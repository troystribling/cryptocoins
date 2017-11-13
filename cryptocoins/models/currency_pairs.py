from peewee import Model, PostgresqlDatabase, DateTimeField, TextField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CurrencyPairs(BaseModel):
    created_at = DateTimeField()
    cryptocompare_subscription = TextField(null=True)
    from_symbol = TextField(index=True, null=True)
    to_symbol = TextField(index=True, null=True)

    class Meta:
        db_table = 'currency_pairs'
        indexes = (
            (('from_symbol', 'to_symbol'), True),
        )

    @classmethod
    def create_from_cryptocompare_ticker_subscription(cls, ticker_sub):
        components = ticker_sub.split("~")
        if len(components) > 3:
            cls.create(cryptocompare_subscription=ticker_sub, from_symbol=components[2], to_symbol=components[3])
