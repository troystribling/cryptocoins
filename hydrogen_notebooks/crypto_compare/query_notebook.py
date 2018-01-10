# %%
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy
import pandas

from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins import Coins
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.collections import Collections
from cryptocoins.models.imports import Imports
from cryptocoins.models.currencies import Currencies

from cryptocoins.crypto_compare.requests import coin_price_history_url

# coins
# %%
query = "SELECT symbol, crypto_compare_rank FROM coins ORDER BY crypto_compare_rank ASC LIMIT %s"
for coin in Coins.raw(query, 10):
    print(coin.symbol, coin.crypto_compare_rank)

# currency_pairs_history
# %%
query = "SELECT * FROM currency_pairs_history" \
        " WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM currency_pairs_history)" \
        "  AND from_symbol = %s ORDER BY volume_from_24_hour DESC LIMIT %s"

for pair in CurrencyPairsHistory.raw(query, 'BTC', 10):
    print(pair.created_at, pair.exchange, pair.from_symbol, pair.to_symbol, pair.volume_from_24_hour)

for currency in CurrencyPairsHistory.fiat_currencies():
    print(currency)

# %%
timestamps = CurrencyPairsHistory.timestamps()
pairs_data_frame = CurrencyPairsHistory.pairs_for_timestamp_epoc_data_frame(timestamps[0], limit=10)
print(pairs_data_frame)

pairs_to_symbol_count = pairs_data_frame.groupby(['from_symbol'])
print(pairs_to_symbol_count.count())

pairs_to_symbol_count = pairs_data_frame['to_symbol'].groupby(pairs_data_frame['from_symbol']).count()
pairs_to_symbol_count.name = 'to_symbol_count'
print(pairs_to_symbol_count)
print(pairs_to_symbol_count.sort_values(ascending=False))
print(pairs_to_symbol_count['42'])
pairs_to_symbol_count.index
pairs_to_symbol_count.values
pairs_to_symbol_count_frame = pairs_to_symbol_count.to_frame()
type(pairs_to_symbol_count_frame)

pairs_to_symbol_volume_sum = pairs_data_frame['volume_from_24_hour'].groupby(pairs_data_frame['from_symbol']).sum()
type(pairs_to_symbol_volume_sum)
print(pairs_to_symbol_volume_sum)

# exchanges_history
# %%
query = "SELECT * FROM exchanges_history" \
        " WHERE timestamp_epoc = (SELECT MAX(timestamp_epoc) FROM exchanges_history)" \
        "  AND from_symbol = %s AND to_symbol = %s ORDER BY volume_from_24_hour DESC LIMIT %s"

for exchange in ExchangesHistory.raw(query, 'BTC', 'USD', 10):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)

# collections
# %%
query = "SELECT created_at FROM collections WHERE url = %s AND success = 'true' ORDER BY created_at LIMIT 1"
url_first = coin_price_history_url('BTC', 'USD', allData='true')
(collection_date) = Collections.raw(query, url_first).scalar()
current_time = datetime.utcnow()
time_delta = current_time - collection_date
time_delta.days

# imports
# %%
latest_date_imports = Collections.raw("SELECT date_dir, MAX(created_at) AS created_at, path"
                                      " FROM imports"
                                      "  GROUP BY date_dir, path, success"
                                      "   HAVING path='cryptocoins/cryptocompare/coin_list'"
                                      "    AND success=TRUE"
                                      " ORDER BY created_at DESC LIMIT 1")
last_import = [last_import for last_import in latest_date_imports]
len(last_import)
parse(last_import[0].date_dir)
parse(last_import[0].date_dir) + timedelta(days=1)

print(Imports.last_import_date_for_path('cryptocoins/cryptocompare/coin_list') + timedelta(days=1))

# coins
# %%
for coin in Coins.top_coins(limit=10):
    print(coin.symbol, coin.crypto_compare_rank)

# currencies
# %%
Currencies.create_for_symbols()
