# %%
%matplotlib inline
%reload_ext autoreload
%autoreload 2

%aimport numpy
from datetime import datetime

from cryptocoins.models.currency_pairs_history import CurrencyPairsHistory
from cryptocoins.models.coins_price_history import CoinsPriceHistory
from cryptocoins.models.exchanges_history import ExchangesHistory
from coin_plots import rank_plots
from coin_plots import timeseries_plots

# %%
timestamps = CurrencyPairsHistory.timestamps()
pairs_data_frame = CurrencyPairsHistory.pairs_for_timestamp_epoc_data_frame(timestamps[0])
from_symbol_count = rank_plots.count_and_rank(pairs_data_frame, 'from_symbol', 'to_symbol')
rank_plots.count_and_rank_plot(from_symbol_count)

# %%
histoday = CoinsPriceHistory.history_data_frame('BTC', 'USD')
close_price_24_hour = histoday['close_price_24_hour']
close_price_24_hour.name = 'BTC'
timeseries_plots.semilog(close_price_24_hour, 'BTC to USD CCCAGG Daily Close')

# %%
histoday = CoinsPriceHistory.history_data_frame('BTC', 'CAD')
close_price_24_hour = histoday['close_price_24_hour']
close_price_24_hour.name = 'BTC'
timeseries_plots.semilog(close_price_24_hour, 'BTC to CAD CCCAGG Daily Close')

# %%
timestamps = ExchangesHistory.timestamps()
timestamps[0]
exchanges = ExchangesHistory.for_timestamp_epoc_data_frame(timestamps[3], from_symbol='BTC')
price = exchanges.close_price_24_hour
exchanges.index
exchanges.loc['Coinbase', ['from_symbol', 'to_symbol', 'close_price_24_hour']]
