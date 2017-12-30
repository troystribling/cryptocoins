# %%
import pandas
from cryptocoins.models.coins import Coins

# %%
for coin in Coins.top_coins():
    print(coin.symbol)
