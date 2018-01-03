import json
from cryptocoins.collect_data import fetch_url_and_upload_to_s3


# fetchers
@fetch_url_and_upload_to_s3
def fetch_and_return(params):
    return [params['response']]


@fetch_url_and_upload_to_s3
def fetch_and_timestamp(params):
    parsed_response = json.loads(params['response'])
    parsed_response['timestamp_epoc'] = params['timestamp_epoc']
    new_result = json.dumps(parsed_response)
    return [new_result]


@fetch_url_and_upload_to_s3
def fetch_histoday(params):
    parsed_response = json.loads(params['response'])
    parsed_response['CurrencyTo'] = params['to_currency']
    parsed_response['CurrencyFrom'] = params['from_currency']
    parsed_response['Exchange'] = params['exchange']
    new_result = json.dumps(parsed_response)
    return [new_result]


# request urls
def coin_list_url():
    return 'https://min-api.cryptocompare.com/data/all/coinlist'


def top_currency_pairs_url(from_currency, limit=100):
    return f"https://min-api.cryptocompare.com/data/top/pairs?fsym={from_currency}&limit={limit}"


def coin_snapshot_url(from_currency, to_currency):
    return f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"


def coin_price_history_url(from_currency, to_currency, limit=1, exchange="CCCAGG", allData='false', app_name='gly.fish'):
    return f"https://min-api.cryptocompare.com/data/histoday?fsym={from_currency}&tsym={to_currency}&limit={limit}&e={exchange}&allData={allData}&extraParams={app_name}"


# requests
def request_coin_list(bucket_name, timestamp_epoc):
    url = coin_list_url()
    path = "cryptocoins/cryptocompare/coin_list"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path, timestamp_epoc=timestamp_epoc)


def request_coin_snapshot(bucket_name, from_currency, to_currency, timestamp_epoc):
    url = coin_snapshot_url(from_currency, to_currency)
    path = 'cryptocoins/cryptocompare/coin_snapshot'
    meta = f"{from_currency}/{to_currency}"
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path, to_currency=to_currency, meta=meta, timestamp_epoc=timestamp_epoc)


def request_coin_price_history(bucket_name, from_currency, to_currency, limit=1, exchange='CCCAGG', allData=False):
    url = coin_price_history_url(from_currency, to_currency, limit=limit, exchange=exchange, allData=allData)
    path = 'cryptocoins/cryptocompare/histoday'
    meta = f"{exchange}/{from_currency}/{to_currency}"
    fetch_histoday(url=url, bucket_name=bucket_name, path=path, to_currency=to_currency, from_currency=from_currency, exchange=exchange, meta=meta)


def request_top_currency_pairs(bucket_name, from_currency, timestamp_epoc, limit=100):
    url = top_currency_pairs_url(from_currency, limit=limit)
    path = 'cryptocoins/cryptocompare/top_pairs'
    meta = from_currency
    fetch_and_timestamp(url=url, bucket_name=bucket_name, path=path, meta=meta, timestamp_epoc=timestamp_epoc)
