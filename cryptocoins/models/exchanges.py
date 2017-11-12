from peewee import Model, PostgresqlDatabase, DateTimeField, TextField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Exchanges(BaseModel):
    created_at = DateTimeField()
    name = TextField(null=True, unique=True)

    class Meta:
        db_table = 'exchanges'

    @classmethod
    def create_from_cryptocompare_ticker_subscription(cls, ticker_sub):
        components = ticker_sub.split("~")
        if len(components) > 1:
            cls.create(name=components[1])
