from time import sleep
import asyncio
from concurrent.futures import ThreadPoolExecutor

from cryptocoins.export_data import fetch_url_and_upload_to_s3
from cryptocoins.models.coins import Coins

thread_pool = ThreadPoolExecutor(max_workers=20)
loop = asyncio.get_event_loop()


async def poll_coin_list():
        while True:
            loop.run_in_executor(thread_pool, coin_list)
            await asyncio.sleep(86400)


async def poll_coin_snapshot_full(coin_limit):
    while True:
        for coin in Coins.select().order_by(Coins.rank.asc()).limit(coin_limit):
            loop.run_in_executor(thread_pool, coin_snapshot_full, coin)
            await asyncio.sleep(60)
        await asyncio.sleep(300)


@fetch_url_and_upload_to_s3
def fetch_and_return(response):
    return [response]


@fetch_url_and_upload_to_s3
def fetch_histoday(response):
    parsed_response = json.loads(response)
    parsed_response['CurrencyTo'] = to_currency
    parsed_response['CurrencyFrom'] = from_currency
    parsed_response['Exchange'] = exchange
    new_result = json.dumps(parsed_response)
    return [new_result]


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    path = "cryptocoins/cryptocompare/coin_snapshot"
    fetch_and_return(url=url, bucket=bucket, path=path)


def coin_snapshot(from_currency, to_currency):
    url = f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"
    path = 'cryptocoins/cryptocompare/coin_snapshot'
    fetch_and_return(url=url, bucket=bucket, path=path)x


def coin_price_history(from_currency, to_currency, limit=1, exchange="CCCAGG", allData=false):
    url = f"https://min-api.cryptocompare.com/data/histoday?fsym={from_currency}&tsym={to_currency}&limit={limit}&e={exchange}&allData={allData}"
    path = 'cryptocoins/cryptocompare/coin_price_history'
    fetch_histoday(url=url, bucket=bucket, path=path)


def top_currency_pairs(from_currency, limit=1000):
    url = f"https://min-api.cryptocompare.com/api/data/top/pairs?fsym={from_currency}&limit={limit}"
    path = 'cryptocoins/cryptocompare/top_pairs'
    fetch_and_return(url=url, bucket=bucket, path=path)x

if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(poll_coin_list(), poll_coin_snapshot_full(10)))
