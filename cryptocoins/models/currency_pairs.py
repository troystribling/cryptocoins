from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, IntegrityError

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
    def create_using_cryptocompare_subscription(cls, subscription):
        components = subscription.split("~")
        if len(components) > 3:
            try:
                with database.atomic():
                    return cls.create(cryptocompare_subscription=subscription, from_symbol=components[2], to_symbol=components[3])
            except IntegrityError:
                return None
