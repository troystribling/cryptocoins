from time import sleep
import asyncio
from concurrent.futures import ThreadPoolExecutor

from cryptocoins import export_data
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


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    print(f"FETCH COIN LIST FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
    else:
        print("ERROR: coint_list request failed")


def coin_snapshot_full(coin):
    url = f"https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={coin.cryptocompare_id}""
    print(f"FETCH FULL COIN SNAP SHOT FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_snapshot_full', [result])
    else:
        print(f"ERROR: coin_snapshot_full request failed for currency {coin.cryptocompare_id}")


def coin_snapshot(from_currency, to_currency):
    url = f"https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={from_currency}&tsym={to_currency}"
    print(f"FETCH COIN SNAP SHOT FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_snapshot', [result])
    else:
        print(f"ERROR: coin_snapshot_full request failed for currencies: {from_currency}, {to_currency}")


def coin_price_history(from_currency, to_currency, limit=1, exchange="CCCAGG", allData=false):
    url = f"https://min-api.cryptocompare.com/api/data/histoday?fsym={from_currency}&tsym={to_currency}&limit={limit}&e={exchange}&allData={allData}"
    print(f"FETCH COIN PRICE HISTORY FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_price_history', [result])
    else:
        print(f"ERROR: coin_price_history request failed for currencies {from_currency}, {to_currency}")


def top_currency_pairs(from_currency, limit=1000):
    url = f"https://min-api.cryptocompare.com/api/data/top/pairs?fsym={from_currency}&limit={limit}"
    print(f"FETCH TOP CURRNCY PAIRS FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/top_currency_pairs', [result])
    else:
        print(f"ERROR: coin_snapshot_full request failed for currency {from_currency}")


if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(poll_coin_list(), poll_coin_snapshot_full(10)))
