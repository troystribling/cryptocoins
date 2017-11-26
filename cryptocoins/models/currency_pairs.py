from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CurrencyPairs(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField(index=True)
    rank = BigIntegerField()
    to_symbol = TextField(index=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'currency_pairs'
        indexes = (
            (('from_symbol', 'to_symbol'), True),
        )

    @classmethod
    def create_using_cryptocompare_subscription(cls, subscription):
        components = subscription.split("~")
        if len(components) > 3:
            try:
                with database.atomic():
                    return cls.create(cryptocompare_subscription=subscription, from_symbol=components[2], to_symbol=components[3])
            except IntegrityError:
                print(f"ERROR: CURRENCY PAIR EXISTS: {subscription}")
                return None
