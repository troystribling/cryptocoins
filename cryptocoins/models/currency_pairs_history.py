from peewee import Model, PostgresqlDatabase, DateTimeField, TextField, DecimalField

from cryptocoins.utils import valid_params


database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CurrencyPairsHistory(BaseModel):
    created_at = DateTimeField()
    from_symbol = TextField(index=True)
    to_symbol = TextField(index=True)
    exchange = TextField()
    volume_from_24_hour = DecimalField()
    volume_to_24_hour = DecimalField()

    class Meta:
        db_table = 'currency_pairs_history'
        indexes = (
            (('from_symbol', 'to_symbol'), False),
        )

    @classmethod
    def create_from_top_pairs(cls, top_pairs, batch_size=100):
        with database.atomic():
            for i in range(0, len(top_pairs), batch_size):
                model_params = [cls.top_pairs_to_model_params(top_pair) for top_pair in top_pairs[i:i + batch_size]]
                cls.insert_many(model_params).execute()

    @classmethod
    def top_pairs_to_model_params(cls, top_pair):
        expected_keys = ['exchange', 'fromSymbol', 'toSymbol', 'volume24h', 'volume24hTo']
        if not valid_params(expected_params=expected_keys, params=top_pair):
            raise ValueError('ERROR: Top Pairs keys invalid')
        return {'from_symbol': top_pair['fromSymbol'],
                'to_symbol': top_pair['toSymbol'],
                'exchange': top_pair['exchange'],
                'volume_from_24_hour': top_pair['volume24h'],
                'volume_to_24_hour': top_pair['volume24hTo']}
