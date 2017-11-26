from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, BigIntegerField, DecimalField


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class ExchangesHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField()
    high_price_24_hour = DecimalField()
    low_price_24_hour = DecimalField()
    name = TextField(index=True)
    open_price_24_hour = DecimalField()
    timestamp = DateTimeField()
    timestamp_epoc = BigIntegerField()
    to_symbol = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'exchanges_history'

    @classmethod
    def create_from_coin_snapshot(cls, coin_snapshot, batch_size=100):
        if 'Exchanges' not in coin_snapshot:
            print("ERROR: Exchanges KEY IS MISSING FROM import_coin_snapshot_full")
            return
        exchanges = coin_snapshot['Exchanges']
        with database.atomic():
            for i in range(0, len(aggredated_data), batch_size):
                model_params = [cls.coin_snapshot_exchange_to_model_params(exchanges) for exchange in exchanges[i:i*batch_size]]
                cls.insert_many(model_params).execute

    @classmethod
    def coin_snapshot_exchange_to_model_params(cls, coin_snapshot):
        return {from_symbol: coin_snapshot['FROMSYMBOL'],
                high_price_24_hour:,
                low_price_24_hour:,
                name:,
                open_price_24_hour:,
                timestamp:,
                timestamp_epoc:,
                to_symbol:,
                volume_from_24_hour:,
                volume_to_24_hour:}
