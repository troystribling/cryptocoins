from peewee import Model, PostgresqlDatabase, IntegrityError, DataError, DateTimeField, TextField
import logging

logger = logging.getLogger(__name__)
database = PostgresqlDatabase('cryptocoins', **{'user': 'cryptocoins'})


class BaseModel(Model):
    class Meta:
        database = database


class CurrenciesInfo(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    name = TextField(null=True)
    currency_type = TextField()
    symbol = TextField(unique=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'currencies_info'

    @classmethod
    def create_for_symbols(cls, symbols, currency_type, batch_size=100):
        if symbols is None:
            logger.error("symbols IS None")
            return
        for i in range(0, len(symbols), batch_size):
            model_params = [cls.symbols_to_model_params(symbol, currency_type) for symbol in symbols[i:i + batch_size]]
            try:
                cls.insert_many(model_params).execute()
            except (IntegrityError, DataError) as error:
                logger.error(f"DATABASE ERROR for CurrenciesInfo: {error}")
                continue

        @classmethod
        def symbols_to_model_params(cls, symbol, currency_type):
            return {'symbol': symbol,
                    'currency_type': currency_type}

        @classmethod
        def get_for_symbol(cls, symbol):
            try:
                return cls.get(CurrenciesInfo.symbol == symbol)
            except IntegrityError as error:
                logger.error(f"DATABASE ERROR FOR CurrenciesInfo with symbol: {symbol}:{error}")
                return None
