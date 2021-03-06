from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField, BigIntegerField, DecimalField
import logging

from cryptocoins.utils import valid_params, null_param_if_missing

logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', user='cryptocoins', host='127.0.0.1')


class BaseModel(Model):
    class Meta:
        database = database


class CoinsHistory(BaseModel):
    algorithm = TextField(null=True)
    block_number = BigIntegerField(null=True)
    block_reward = DecimalField(null=True)
    created_at = DateTimeField(null=True)
    high_price_24_hour = DecimalField(null=True)
    low_price_24_hour = DecimalField(null=True)
    net_hashes_per_second = DecimalField(null=True)
    open_price_24_hour = DecimalField(null=True)
    close_price_24_hour = DecimalField(null=True)
    proof_type = TextField(null=True)
    from_symbol = TextField(index=True)
    to_symbol = TextField(index=True)
    last_update_epoc = BigIntegerField()
    timestamp_epoc = DecimalField()
    total_coins_mined = DecimalField()
    volume_from_24_hour = DecimalField(null=True)
    volume_to_24_hour = DecimalField(null=True)

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
                cls.create(**coin_snapshot)
            except (IntegrityError, DataError) as error:
                logger.error(f"DATABASE ERROR for CoinsHistory: {error}")

    @classmethod
    def coin_snapshot_to_model_parameters(cls, data):
        expected_keys = ['timestamp_epoc', 'Data']
        if not valid_params(expected_params=expected_keys, params=data):
            logger.error('coin_snapshot KEYS INVALID')
            return None
        coin_snapshot = data['Data']
        expected_keys = ['Algorithm', 'BlockNumber', 'BlockReward', 'NetHashesPerSecond', 'ProofType', 'TotalCoinsMined']
        null_param_if_missing(expected_params=expected_keys, params=coin_snapshot)

        if 'AggregatedData' not in coin_snapshot:
            logger.error(f"AggregatedData KEY IS MISSING FROM coin_snapshot: {coin_snapshot}")
            return None
        aggregated_data = coin_snapshot['AggregatedData']

        expected_keys = ['FROMSYMBOL', 'TOSYMBOL', 'LOW24HOUR', 'OPEN24HOUR', 'LASTUPDATE',
                         'HIGH24HOUR', 'VOLUME24HOUR', 'VOLUME24HOURTO', 'PRICE']
        if not valid_params(expected_params=expected_keys, params=aggregated_data):
            return None

        timestamp_epoc = data['timestamp_epoc']
        last_update_epoc = aggregated_data['LASTUPDATE']

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
                'last_update_epoc': last_update_epoc}

    @classmethod
    def history(cls, from_symbol, to_symbol=None):
        if to_symbol is None:
            return cls.raw("SELECT * FROM coins_history WHERE from_symbol = %s"
                           " ORDER BY timestamp_epoc DESC", from_symbol)
        else:
            return cls.raw("SELECT * FROM coins_history WHERE from_symbol = %s AND to_symbol = %s"
                           " ORDER BY timestamp_epoc DESC LIMIT %s", timestamp_epoc, to_symbol, )

    @classmethod
    def history_data_frame(cls, from_symbol, to_symbol=None):
        records = [record for record in cls.history(from_symbol, to_symbol).dicts()]
        index = [record['last_update_epoc'] for record in records]
        return pandas.DataFrame(records, index=index)
