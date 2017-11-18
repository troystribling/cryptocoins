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
            await asyncio.sleep(300)


async def poll_coin_snapshot_full(coin_limit):
    while True:
        for coin in Coins.select().order_by(Coins.rank.asc()).limit(coin_limit):
            loop.run_in_executor(thread_pool, coin_snapshot_full, coin)
            await asyncio.sleep(60)
        await asyncio.sleep(86400)


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    print(f"FETCH COIN LIST FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
    else:
        print("ERROR: coint_list request failed")


def coin_snapshot_full(coin):
    url = f'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={coin.cryptocompare_id}'
    print(f"FETCH COIN SNAP SHOT FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_snapshot_full', [result])
    else:
        print(f"ERROR: coin_snapshot_full request failed for currency {coin.cryptocompare_id}")


if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(poll_coin_list(), poll_coin_snapshot_full(10)))
