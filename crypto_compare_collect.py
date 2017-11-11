from time import sleep
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue

from cryptocoins import export_data

thread_pool = ThreadPoolExecutor(max_workers=20)
loop = asyncio.get_event_loop()

async def poll_coinlist():
        while True:
            loop.run_in_executor(thread_pool, coin_list)
            await asyncio.sleep(300)


async def poll_coin_snapshot_full():
    while True:
        loop.run_in_executor(thread_pool, coin_snapshot_full)
        await asyncio.sleep(300)


def coin_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    print(f"FETCH COIN LIST FROM: {url}")
    result = export_data.getURL(url)
    if result is not None:
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
    else:
        print("ERROR: coint_list request failed")


def coin_snapshot_full():
    currencies = [1182, 7605]
    for currency in currencies:
        url = f'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={currency}'
        print(f"FETCH COIN SNAP SHOT FROM: {url}")
        result = export_data.getURL(url)
        if result is not None:
            export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_snapshot_full', [result])
        else:
            print(f"ERROR: coin_snapshot_full request failed for currency {currency}")
        sleep(30)


if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(poll_coinlist(), poll_coin_snapshot_full()))
