# %%
import tempfile
import os
from dateutil.parser import parse
import json

from cryptocoins import export_data

# %%
from_currency = 'BTC'
to_currency = 'USD'
url = f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"
result = export_data.fetch_url(url)
parsed_result = json.loads(result)

# %%
from_currency = 'BTC'
to_currency = 'USD'
limit = 100
allData = "false"
exchange = "CCCAGG"
url = f"https://min-api.cryptocompare.com/data/histoday?fsym={from_currency}&tsym={to_currency}&e={exchange}&allData={allData}"
result = export_data.fetch_url(url)
parsed_result = json.loads(result)
parsed_result[]

# %%
from_currency = 'BTC'
limit = 100
url = f"https://min-api.cryptocompare.com/api/data/top/pairs?fsym={from_currency}&limit={limit}"
result = export_data.fetch_url(url)
