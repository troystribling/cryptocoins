# %%
%matplotlib inline
%reload_ext autoreload
%autoreload 2

import numpy
from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from coin_plots import rank_plots

# %%
timestamps = CurrencyPairsHistory.timestamps()
pairs_data_frame = CurrencyPairsHistory.pairs_for_timestamp_epoc_data_frame(timestamps[0])
from_symbol_count = rank_plots.count_and_rank(pairs_data_frame, 'from_symbol', 'to_symbol')
rank_plots.count_and_rank_plot(from_symbol_count)
