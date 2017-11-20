from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, IntegrityError, BigIntegerField, DecimalField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Exchanges(BaseModel):
    created_at = DateTimeField()
    name = TextField(unique=True)
    rank = BigIntegerField()
    updated_at = DateTimeField()
    volume_usd = DecimalField()

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
                return None
