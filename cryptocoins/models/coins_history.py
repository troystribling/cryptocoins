from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database

class CoinsHistory(BaseModel):
    algorithm = TextField()
    block_number = BigIntegerField()
    block_reward = DecimalField()
    created_at = DateTimeField()
    net_hashes_per_second = DecimalField()
    proof_type = TextField()
    symbol = TextField(index=True)
    total_coins_mined = DecimalField()

    class Meta:
        db_table = 'coins_history'
