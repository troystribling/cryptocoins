from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CoinsHistory(BaseModel):
    algorithm = TextField()
    block_number = BigIntegerField()
    block_reward = DecimalField()
    created_at = DateTimeField()
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    net_hashes_per_second = DecimalField()
    open_price_24_hour = DecimalField()
    proof_type = TextField()
    symbol = TextField(index=True)
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    total_coins_mined = DecimalField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'coins_history'

    @classmethod
    def create_from_coin_snapshot(cls, coin_snapshot):
        expected_keys = ['Algorithm', 'BlockNumber', 'BlockReward', 'NetHashesPerSecond', 'ProofType', 'TotalCoinsMined', 'Symbol']
        for expected_key in expected_keys:
            if expected_key not in coin_snapshot:
                print(f"ERROR: '{expected_key}' KEY IS MISSING FROM coin_snapshot")
                return

        with database.atomic():
            cls.create(algorithm=coin_snapshot['Algorithm'],
                       block_number=coin_snapshot['BlockNumber'],
                       block_reward=coin_snapshot['BlockReward'],
                       net_hashes_per_second=coin_snapshot['NetHashesPerSecond'],
                       proof_type=coin_snapshot['ProofType'],
                       symbol=coin_snapshot['Symbol'],
                       total_coins_mined=coin_snapshot['TotalCoinsMined'])
