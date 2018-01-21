import json
from datetime import timedelta, datetime

from cryptocoins.collect_data import fetch_url_and_upload_to_s3

# fetchers
@fetch_url_and_upload_to_s3
def fetch_and_return(params):
    return [params['response']]



# request urls
def from_usd_url(api_key, to_symbol):
    return f"https://forex.1forge.com/1.0.2/convert?from=USD&to={to_symbol}&quantity=1&api_key={api_key}"

# requests
def request_from_usd(bucket_name, api_key, to_symbol):
    url = from_usd_url(api_key, to_symbol)
    path = "forex/1forge/usd_rates"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path)
