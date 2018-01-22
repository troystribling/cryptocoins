import json
from datetime import timedelta, datetime

from cryptocoins.collect_data import fetch_url_and_upload_to_s3

# fetchers
@fetch_url_and_upload_to_s3
def fetch(params):
    return [[params['response']]]


# request urls
def latest_exchange_rate_url(from_symbol):
    return f"https://api.fixer.io/latest?base={from_symbol}"


def exchange_rate_for_date_url(date, from_symbol):
    request_date = date.strftime('%Y-%m-%d')
    return f"https://api.fixer.io/{request_date}?base={from_symbol}"

# requests
def request_latest_exchange_rate(bucket_name, from_symbol):
    url = latest_exchange_rate_url(from_symbol)
    path = "forex/fixer/exchange_rates"
    meta = f"{from_symbol}"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path)


def request_exchange_rate(bucket_name, date, from_symbol):
    url = exchange_rate_for_date_url(date, from_symbol)
    path = "forex/fixer/exchange_rates"
    meta = f"{from_symbol}"
    fetch(url=url, bucket_name=bucket_name, path=path, meta=meta)
