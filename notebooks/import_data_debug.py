from dateutil.parser import parse
import tempfile
import os

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.import_data import read_from_file

from cryptocoins.models.exchanges_history import ExchangesHistory
from cryptocoins.models.coins_history import CoinsHistory

start_date = parse('20171210')
end_date = parse('20171210')

# %%

import_coin_snapshot(start_date, end_date)

# %%
local_file_path = "cryptocoins/cryptocompare/coin_snapshot/20171210/20171210-173000-9wb_2k6d"
tempdir = tempfile.gettempdir()
file_path = os.path.join(tempdir, local_file_path)
data = read_from_file(file_path)
coin_snapshot = data[0]
CoinsHistory.create_from_coin_snapshot(coin_snapshot)
ExchangesHistory.create_from_coin_snapshot(coin_snapshot)
