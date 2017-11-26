# %%
import json

from cryptocoins.export_data import fetch_url_and_upload_to_s3

bucket = 'gly.fish'
from_currency = 'BTC'
to_currency = 'USD'
limit = 100

# coin_snapshot
# %%
url = f"https://min-api.cryptocompare.com/data/all/coinlist"
path = "cryptocoins/cryptocompare/coin_list"


@fetch_url_and_upload_to_s3
def fetch_coin_list(params):
    return [params['response']]


fetch_coin_list(url=url, bucket=bucket, path=path)

# coin_snapshot
# %%
url = f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"
path = "cryptocoins/cryptocompare/coin_snapshot"


@fetch_url_and_upload_to_s3
def fetch_coin_snapshot(params):
    parsed_response = json.loads(params['response'])
    parsed_response['Symbol'] = params['to_currency']
    new_result = json.dumps(parsed_response)
    return [new_result]


fetch_coin_snapshot(url=url, bucket=bucket, path=path, to_currency=to_currency)

# top_pairs
# %%
url = f"https://min-api.cryptocompare.com/data/top/pairs?fsym={from_currency}&limit={limit}"
path = "cryptocoins/cryptocompare/top_pairs"


@fetch_url_and_upload_to_s3
def fetch_top_pairs(params):
    return [params['response']]


fetch_top_pairs(url=url, bucket=bucket, path=path)

# histoday
# %%
allData = True
exchange = "CCCAGG"
path = "cryptocoins/cryptocompare/histoday"
url = f"https://min-api.cryptocompare.com/data/histoday?fsym={from_currency}&tsym={to_currency}&e={exchange}&allData={allData}"


@fetch_url_and_upload_to_s3
def fetch_histoday(params):
    parsed_response = json.loads(params['response'])
    parsed_response['CurrencyTo'] = params['to_currency']
    parsed_response['CurrencyFrom'] = params['from_currency']
    parsed_response['Exchange'] = params['exchange']
    new_result = json.dumps(parsed_response)
    return [new_result]


fetch_histoday(url=url, bucket=bucket, path=path, to_currency=to_currency, from_currency=from_currency, exchange=exchange)
