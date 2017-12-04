# %%
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins import Coins
from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory
from cryptocoins.models.collections import Collections


# %% coins
for coin in Coins.raw('SELECT * FROM coins ORDER By rank ASC'):
    print(coin.symbol)

# %% exchanges_history
for exchange in ExchangesHistory.raw('SELECT * FROM exchanges_history ORDER BY volume_from_24_hour DESC'):
    print(exchange.name, exchange.from_symbol, exchange.to_symbol, exchange.volume_from_24_hour)
