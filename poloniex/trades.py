import asyncio
import aiohttp
from time import time
import sys

import itertools

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import import_data, export_data

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)

results_per_file = 5
poll_seconds = 10.0
currency_pairs = ['BTC_ETH']

async def poll():
    total_results_count = 0
    results = []
    end_time = time()
    while True:
        total_results_count += 1
        for currency_pair in currency_pairs:
            url = f'https://poloniex.com/public?command=returnTradeHistory&currencyPair={currency_pair}&start={end_time - poll_seconds}&end={end_time}'
            end_time += poll_seconds
            result = await import_data.http_get(session, url)
            results.append(result.decode("utf-8"))
            await asyncio.sleep(poll_seconds)
        if total_results_count % results_per_file == 0:
            export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/trades', results)
            results = []

loop.run_until_complete(poll())
