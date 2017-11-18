from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, IntegrityError, BigIntegerField

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class Coins(BaseModel):
    coin_name = TextField(null=True)
    created_at = DateTimeField()
    cryptocompare_id = BigIntegerField(null=True)
    full_name = TextField(null=True)
    name = TextField(null=True)
    rank = BigIntegerField(null=True)
    symbol = TextField(null=True, unique=True)

    class Meta:
        db_table = 'coins'

    @classmethod
    def create_using_crytocompare_coinlist(cls, coin_list):
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
                return cls.create(coin_name=coin_list['CoinName'],
                                  cryptocompare_id=coin_list['Id'],
                                  full_name=coin_list['FullName'],
                                  name=coin_list['Name'],
                                  symbol=coin_list['Symbol'],
                                  rank=coin_list['SortOrder'])
            print(f"CREATED COIN: {coin_list['Symbol']}")
        except IntegrityError:
            return None
