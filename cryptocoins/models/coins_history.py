from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime

from cryptocoins.utils import valid_params

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
    close_price_24_hour = DecimalField()
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
        expected_keys = ['Algorithm', 'BlockNumber', 'BlockReward',
                         'NetHashesPerSecond', 'ProofType', 'TotalCoinsMined']
        if not valid_params(expected_params=expected_keys, params=coin_snapshot)
            return

        aggregated_data = coin_snapshot['AggregatedData']
        expected_keys = ['FROMSYMBOL', 'LOW24HOUR', 'OPEN24HOUR', 'LASTUPDATE',
                         'HIGH24HOUR', 'VOLUM24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=aggregated_data)
            return

        timestamp_epoc = aggregated_data['LASTUPDATE']
        with database.atomic():
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
                              close_price_24_hour=aggregated_data['PRICE']
                              volume_from_24_hour=aggregated_data['VOLUM24HOUR'],
                              volume_to_24_hour=aggregated_data['VOLUME24HOURTO'],
                              timestamp_epoc=timestamp_epoc,
                              timestamp=datetime.fromtimestamp(int(timestamp_epoc)))
