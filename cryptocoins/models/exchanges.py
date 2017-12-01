from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Exchanges(BaseModel):
    created_at = DateTimeField()
    name = TextField(unique=True)
    updated_at = DateTimeField()
    volume_total_usd = DecimalField()

    class Meta:
        db_table = 'exchanges'

    @classmethod
    def create_using_cryptocompare_subscription(cls, ticker_sub):
        components = ticker_sub.split("~")
        if len(components) > 1:
            try:
                with database.atomic():
                    return cls.create(name=components[1])
            except IntegrityError:
                print(f"ERROR: EXCHANGE EXISTS: {ticker_sub}")
                return None
