# %%
import json

from cryptocoins.export_data import fetch_url_and_upload_to_s3

bucket = 'gly.fish'
from_currency = 'BTC'
to_currency = 'USD'
limit = 100

# %%
url = f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"
path = "cryptocoins/cryptocompare/coin_snapshot"


@fetch_url_and_upload_to_s3
def fetch_coin_snapshot(response):
    return [response]


fetch_coin_snapshot(url=url, bucket=bucket, path=path)

# %%
allData = True
exchange = "CCCAGG"
path = "cryptocoins/cryptocompare/histoday"
url = f"https://min-api.cryptocompare.com/data/histoday?fsym={from_currency}&tsym={to_currency}&e={exchange}&allData={allData}"


@fetch_url_and_upload_to_s3
def fetch_histoday(response):
    parsed_response = json.loads(response)
    parsed_response['CurrencyTo'] = to_currency
    parsed_response['CurrencyFrom'] = from_currency
    parsed_response['Exchange'] = exchange
    new_result = json.dumps(parsed_response)
    return [new_result]


fetch_histoday(url=url, bucket=bucket, path=path)

# %%
url = f"https://min-api.cryptocompare.com/api/data/top/pairs?fsym={from_currency}&limit={limit}"
path = "cryptocoins/cryptocompare/top_pairs"


@fetch_url_and_upload_to_s3
def fetch_top_pairs(result):
    return [result]


fetch_top_pairs(url=url, bucket=bucket, path=path)
