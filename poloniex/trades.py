from time import time, sleep
from urllib.request import urlopen

import sys
if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import export_data

results_per_file = 5
poll_seconds = 10.0
currency_pairs = ['BTC_ETH']

def poll():
    total_results_count = 0
    results = []
    end_time = time()
    while True:
        total_results_count += 1
        for currency_pair in currency_pairs:
            url = f'https://poloniex.com/public?command=returnTradeHistory&currencyPair={currency_pair}&start={end_time - poll_seconds}&end={end_time}'
            end_time += poll_seconds
            response = urlopen(url)
            assert response.status == 200
            result = response.read().decode("utf-8")
            results.append(f'{{"currency_pair":{currency_pair}, "trades":{result}}}')
            sleep(1)
            if total_results_count % results_per_file == 0:
                export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/trades', results)
                results = []
        sleep(poll_seconds)

poll()
