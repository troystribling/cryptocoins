from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

from cryptocoins.utils import valid_params

database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CoinsHistory(BaseModel):
    algorithm = TextField(null=True)
    block_number = BigIntegerField()
    block_reward = DecimalField()
    created_at = DateTimeField()
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    net_hashes_per_second = DecimalField()
    open_price_24_hour = DecimalField()
    close_price_24_hour = DecimalField()
    proof_type = TextField(null=True)
    symbol = TextField(index=True)
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    total_coins_mined = DecimalField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'coins_history'

    @classmethod
    def create_from_coin_snapshot(cls, data):
        if 'Data' not in data:
            print(f"ERROR: Data KEY IS MISSING FROM coin_snapshot: {data}")
            return
        coin_snapshot = data['Data']
        expected_keys = ['Algorithm', 'BlockNumber', 'BlockReward',
                         'NetHashesPerSecond', 'ProofType', 'TotalCoinsMined']
        if not valid_params(expected_params=expected_keys, params=coin_snapshot):
            return

        if 'AggregatedData' not in coin_snapshot:
            print(f"ERROR: Data KEY IS MISSING FROM coin_snapshot: {coin_snapshot}")
            return
        aggregated_data = coin_snapshot['AggregatedData']

        expected_keys = ['FROMSYMBOL', 'LOW24HOUR', 'OPEN24HOUR', 'LASTUPDATE',
                         'HIGH24HOUR', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=aggregated_data):
            return

        timestamp_epoc = aggregated_data['LASTUPDATE']
        with database.atomic():
            try:
                return cls.create(algorithm=coin_snapshot['Algorithm'],
                                  block_number=coin_snapshot['BlockNumber'],
                                  block_reward=coin_snapshot['BlockReward'],
                                  net_hashes_per_second=coin_snapshot['NetHashesPerSecond'],
                                  proof_type=coin_snapshot['ProofType'],
                                  total_coins_mined=coin_snapshot['TotalCoinsMined'],
                                  symbol=aggregated_data['FROMSYMBOL'],
                                  high_price_24_hour=aggregated_data['HIGH24HOUR'],
                                  low_price_24_hour=aggregated_data['LOW24HOUR'],
                                  open_price_24_hour=aggregated_data['OPEN24HOUR'],
                                  close_price_24_hour=aggregated_data['PRICE'],
                                  volume_from_24_hour=aggregated_data['VOLUME24HOUR'],
                                  volume_to_24_hour=aggregated_data['VOLUME24HOURTO'],
                                  timestamp_epoc=timestamp_epoc,
                                  timestamp=datetime.utcfromtimestamp(int(timestamp_epoc)))
            except IntegrityError as error:
                print(f"ERROR: CoinsHistory Update Exists for {coin_snapshot}: {error}")
                return None
            except DataError as error:
                print(f"ERROR: CoinsHistory Precision failure for {coin_snapshot}: {error}")
                return None
