from time import time, sleep
from urllib.request import urlopen

import os
import sys
file_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.join(file_path, '..'))

from cryptocoins import export_data

results_per_file = 100
poll_seconds = 300.0
currency_pairs = ['BTC_ETH', 'USDT_BTC', 'USDT_ETH', 'ETH_GNO', 'BTC_LTC']

def poll():
    total_results_count = 0
    results = []
    start_time = time() - poll_seconds
    while True:
        total_results_count += 1
        for currency_pair in currency_pairs:
            end_time = time()
            url = f'https://poloniex.com/public?command=returnTradeHistory&currencyPair={currency_pair}&start={start_time}&end={end_time}'
            start_time = end_time
            response = urlopen(url)
            if response.status != 200:
                print(f"HTTP ERROR: status = {response.status}")
                continue
            result = response.read().decode("utf-8")
            results.append(f'{{"currency_pair":"{currency_pair}", "trades":{result}}}')
            sleep(1)
        if total_results_count % results_per_file == 0:
            export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/trades', results)
            results = []
        sleep(poll_seconds)

poll()
