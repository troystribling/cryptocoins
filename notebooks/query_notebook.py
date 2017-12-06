# %%
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins import Coins
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory
from cryptocoins.models.collections import Collections


# coins
# %%
query = "SELECT symbol, rank FROM coins ORDER BY rank ASC LIMIT 10"
for coin in Coins.raw(query):
    print(coin.symbol, coin.rank)

# coin_pairs
# %%
query = "SELECT full_table.created_at,  full_table.exchange, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour" \
        " FROM currency_pairs_history AS full_table" \
        " INNER JOIN (SELECT MAX(id) AS latest_id, exchange, from_symbol, to_symbol FROM currency_pairs_history GROUP BY exchange, from_symbol, to_symbol HAVING from_symbol = %s)" \
        " AS latest ON (full_table.id = latest.latest_id) ORDER BY full_table.volume_from_24_hour DESC"

for pair in CurrencyPairsHistory.raw(query, 'BTC'):
    print(pair.created_at, pair.exchange, pair.from_symbol, pair.to_symbol, pair.volume_from_24_hour)

# exchanges_history
# %%
query = "SELECT created_at, name, from_symbol, to_symbol, volume_from_24_hour FROM exchanges_history" \
        " WHERE name = %s"

for exchange in ExchangesHistory.raw(query, 'Bitfinex'):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)

# %%
query = "SELECT created_at, name, from_symbol, to_symbol, volume_from_24_hour FROM exchanges_history" \
        " WHERE name = %s AND from_symbol = %s AND to_symbol = %s"

for exchange in ExchangesHistory.raw(query, 'Bitfinex', 'BTC', 'USD'):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)


# %%
query = "SELECT MAX(created_at), name, from_symbol, to_symbol, volume_from_24_hour FROM exchanges_history" \
        " GROUP BY name, from_symbol, to_symbol, volume_from_24_hour ORDER BY volume_from_24_hour DESC"

for exchange in ExchangesHistory.raw(query, 'Bitfinex'):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)


# %%
query = "SELECT * FROM exchanges_history ORDER BY volume_from_24_hour DESC"
for exchange in ExchangesHistory.raw(query):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)
