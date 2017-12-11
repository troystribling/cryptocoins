# %%
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins import Coins
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory
from cryptocoins.models.collections import Collections


# coins
# %%
query = "SELECT symbol, rank FROM coins ORDER BY rank ASC LIMIT %s"
for coin in Coins.raw(query, limit):
    print(coin.symbol, coin.rank)

# currency_pairs_history
# %%
query = "SELECT full_table.created_at, full_table.exchange, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour" \
        " FROM currency_pairs_history AS full_table" \
        " INNER JOIN" \
        " (SELECT MAX(id) AS latest_id, exchange, from_symbol, to_symbol FROM currency_pairs_history" \
        " GROUP BY exchange, from_symbol, to_symbol HAVING from_symbol = %s)" \
        " AS latest ON (full_table.id = latest.latest_id)" \
        " ORDER BY full_table.volume_from_24_hour DESC LIMIT %s"

for pair in CurrencyPairsHistory.raw(query, 'BTC', 10):
    print(pair.created_at, pair.exchange, pair.from_symbol, pair.to_symbol, pair.volume_from_24_hour)

# exchanges_history
# %%
query = "SELECT full_table.created_at, full_table.name, full_table.from_symbol, full_table.to_symbol, full_table.volume_from_24_hour" \
        " FROM exchanges_history AS full_table" \
        " INNER JOIN" \
        " (SELECT MAX(id) AS latest_id, name, from_symbol, to_symbol FROM exchanges_history GROUP" \
        " BY name, from_symbol, to_symbol HAVING from_symbol = %s AND to_symbol = %s)" \
        " AS latest ON (full_table.id = latest.latest_id)" \
        " ORDER BY full_table.volume_from_24_hour DESC LIMIT %s"

for exchange in ExchangesHistory.raw(query, 'BTC', 'USD', 10):
    print(exchange.created_at, exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)


# collections
# %%
query = "SELECT created_at FROM collections WHERE url = %s AND success = 'true' ORDER BY created_at LIMIT 1"

result = Collections.raw(query, "http://nothing")
result is None
