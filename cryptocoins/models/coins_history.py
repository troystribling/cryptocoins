from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
from datetime import datetime
import logging

from cryptocoins.utils import valid_params

logger = logging.getLogger(__name__)
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
    from_symbol = TextField(index=True)
    to_symbol = TextField(index=True)
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    total_coins_mined = DecimalField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'coins_history'
        indexes = (
            (('from_symbol', 'to_symbol'), False),
        )

    @classmethod
    def create_from_coin_snapshot(cls, data):
        coin_snapshot = cls.coin_snapshot_to_model_parameters(data)
        if coin_snapshot is None:
            return
        with database.atomic():
            try:
                return cls.create(**coin_snapshot)
            except (IntegrityError, DataError) as error:
                logger.error(f"DATABASE ERROR for CoinsHistory: {error}: {coin_snapshot}")
                return None

    @classmethod
    def coin_snapshot_to_model_parameters(cls, data):
        if 'Data' not in data:
            logger.error(f"Data KEY IS MISSING FROM coin_snapshot: {data}")
            return None
        coin_snapshot = data['Data']
        expected_keys = ['Algorithm', 'BlockNumber', 'BlockReward',
                         'NetHashesPerSecond', 'ProofType', 'TotalCoinsMined']
        if not valid_params(expected_params=expected_keys, params=coin_snapshot):
            return None

        if 'AggregatedData' not in coin_snapshot:
            logger.error(f"Data KEY IS MISSING FROM coin_snapshot: {coin_snapshot}")
            return None
        aggregated_data = coin_snapshot['AggregatedData']

        expected_keys = ['FROMSYMBOL', 'TOSYMBOL', 'LOW24HOUR', 'OPEN24HOUR', 'LASTUPDATE',
                         'HIGH24HOUR', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=aggregated_data):
            return None

        timestamp_epoc = aggregated_data['LASTUPDATE']

        return {'algorithm': coin_snapshot['Algorithm'],
                'block_number': coin_snapshot['BlockNumber'],
                'block_reward': coin_snapshot['BlockReward'],
                'net_hashes_per_second': coin_snapshot['NetHashesPerSecond'],
                'proof_type': coin_snapshot['ProofType'],
                'total_coins_mined': coin_snapshot['TotalCoinsMined'],
                'from_symbol': aggregated_data['FROMSYMBOL'],
                'to_symbol': aggregated_data['TOSYMBOL'],
                'high_price_24_hour': aggregated_data['HIGH24HOUR'],
                'low_price_24_hour': aggregated_data['LOW24HOUR'],
                'open_price_24_hour': aggregated_data['OPEN24HOUR'],
                'close_price_24_hour': aggregated_data['PRICE'],
                'volume_from_24_hour': aggregated_data['VOLUME24HOUR'],
                'volume_to_24_hour': aggregated_data['VOLUME24HOURTO'],
                'timestamp_epoc': timestamp_epoc,
                'timestamp': datetime.utcfromtimestamp(int(timestamp_epoc))}
