from peewee import Model, PostgresqlDatabase, IntegrityError, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Coins(BaseModel):
    coin_name = TextField()
    created_at = DateTimeField()
    cryptocompare_id = BigIntegerField()
    full_name = TextField()
    name = TextField()
    rank = BigIntegerField()
    symbol = TextField(unique=True)
    updated_at = DateTimeField()
    volume_total_usd = DecimalField()

    class Meta:
        db_table = 'coins'

    @classmethod
    def create_or_update_using_crytocompare_coinlist(cls, coin_list):
        if 'CoinName' not in coin_list:
            print(f"ERROR: 'CoinName' KEY IS MISSING FROM coin_list {coin_list}")
            return
        if 'Id' not in coin_list:
            print(f"ERROR: 'Id' KEY IS MISSING FROM coin_list {coin_list}")
            return
        if 'FullName' not in coin_list:
            print(f"ERROR: 'FullName' KEY IS MISSING FROM coin_list {coin_list}")
            return
        if 'Name' not in coin_list:
            print(f"ERROR: 'Name' KEY IS MISSING FROM coin_list {coin_list}")
            return
        if 'Symbol' not in coin_list:
            print(f"ERROR: 'Symbol' KEY IS MISSING FROM coin_list {coin_list}")
            return
        if 'SortOrder' not in coin_list:
            print(f"ERROR: 'SortOrder' KEY IS MISSING FROM coin_list {coin_list}")
            return
        try:
            with database.atomic():
                cls.create(coin_name=coin_list['CoinName'],
                           cryptocompare_id=coin_list['Id'],
                           full_name=coin_list['FullName'],
                           name=coin_list['Name'],
                           symbol=coin_list['Symbol'],
                           rank=coin_list['SortOrder'])
        except IntegrityError:
            query = cls.update(updated_at=datetime.utcnow(),
                               rank=coin_list['SortOrder'])
            query.execute()
