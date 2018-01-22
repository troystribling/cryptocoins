import json
from datetime import timedelta, datetime

from cryptocoins.collect_data import fetch_url_and_upload_to_s3

# fetchers
@fetch_url_and_upload_to_s3
def fetch_exchange_rate(params):
    parsed_response = json.loads(params['response'])
    parsed_response['to_symbol'] = params['to_symbol']
    parsed_response['from_symbol'] = params['from_symbol']
    new_result = json.dumps(parsed_response)
    return [new_result]



# request urls
def exchange_rate_url(api_key, from_symbol, to_symbol):
    return f"https://forex.1forge.com/1.0.2/convert?from={from_symbol}&to={to_symbol}&quantity=1&api_key={api_key}"

# requests
def request_exchange_rate(bucket_name, api_key, from_symbol, to_symbol):
    url = from_usd_url(api_key, to_symbol)
    path = "forex/1forge/exchange_rates"
    meta = f"{from_symbol}/{to_symbol}"
    fetch_exchange_rate(url=url, bucket_name=bucket_name, path=path, meta=meta, from_symbol=from_symbol, to_symbol=to_symbol)
