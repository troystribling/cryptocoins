# %%
%matplotlib inline
%reload_ext autoreload
%autoreload 2

%aimport numpy

from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory
from coin_plots import rank_plots

# %%
timestamps = CurrencyPairsHistory.timestamps()
pairs_data_frame = CurrencyPairsHistory.pairs_for_timestamp_epoc_data_frame(timestamps[0])
from_symbol_count = rank_plots.count_and_rank(pairs_data_frame, 'from_symbol', 'to_symbol')
rank_plots.count_and_rank_plot(from_symbol_count)

# %%
histoday = CoinsPriceHistory.history_data_frame('BTC', 'USD')
