import json
from datetime import timedelta, datetime

from cryptocoins.collect_data import fetch_url_and_upload_to_s3

# fetchers
@fetch_url_and_upload_to_s3
def fetch_and_timestamp(params):
    parsed_response = json.loads(params['response'])
    parsed_response['timestamp_epoc'] = params['timestamp_epoc']
    new_result = json.dumps(parsed_response)
    return [new_result]

# request urls
def latest_from_usd_url():
    return 'https://api.fixer.io/latest?base=USD'

def date_from_usd_url(date):
    request_date = date.strftime('%Y-%m-%d')
    return f"https://api.fixer.io/{request_date}?base=USD"

# requests
def request_latest_from_usd(bucket_name, timestamp_epoc):
    url = latest_from_usd_url()
    path = "forex/fixer/usd_rates"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path, timestamp_epoc=timestamp_epoc)

def request_for_date_from_usd(bucket_name, date, timestamp_epoc):
    url = date_from_usd_url(date)
    path = "forex/fixer/usd_rates"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path, timestamp_epoc=timestamp_epoc)
