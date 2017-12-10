from peewee import Model, PostgresqlDatabase, IntegrityError, InternalError, DataError, DateTimeField, TextField, DecimalField

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
    def create_from_top_pairs(cls, data, batch_size=100):
        if 'Data' not in data:
            print(f"ERROR: Data KEY IS MISSING FROM currency_pairs_history: {data}")
            return
        top_pairs = data['Data']
        with database.atomic():
            for i in range(0, len(top_pairs), batch_size):
                model_params = [cls.top_pairs_to_model_params(top_pair) for top_pair in top_pairs[i:i + batch_size]]
                try:
                    cls.insert_many(model_params).execute()
                except (IntegrityError, InternalError) as error:
                    print(f"ERROR: Currency Pair History Update Exists: {error}")
                    continue
                except DataError as error:
                    print(f"ERROR: CurrencyPairsHistory Precision failure for {top_pairs}: {error}")
                    return None


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

    @classmethod
    def currency_pairs_for_coin(cls, coin, limit=10):
        query = "SELECT full_table.created_at, full_table.exchange, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour" \
                " FROM currency_pairs_history AS full_table" \
                " INNER JOIN" \
                " (SELECT MAX(id) AS latest_id, exchange, from_symbol, to_symbol FROM currency_pairs_history" \
                " GROUP BY exchange, from_symbol, to_symbol HAVING from_symbol = %s)" \
                " AS latest ON (full_table.id = latest.latest_id)" \
                " ORDER BY full_table.volume_from_24_hour DESC LIMIT %s"
        return cls.raw(query, coin, limit)
