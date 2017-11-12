from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Coins(BaseModel):
    coin_name = TextField(null=True)
    created_at = DateTimeField()
    cryptocompare = BigIntegerField(db_column='cryptocompare_id', null=True)
    full_name = TextField(null=True)
    name = TextField(null=True)
    symbol = TextField(null=True, unique=True)

    class Meta:
        db_table = 'coins'
