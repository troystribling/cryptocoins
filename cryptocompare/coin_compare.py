from time import time, sleep
from urllib.request import urlopen

import sys
if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import export_data

poll_seconds = 10.0
currencies = [1182, 7605]

def poll():
    results = []
    end_time = time()
    while True:
        for currency in currencies:
            url = f'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={currency}'
            response = urlopen(url)
            if response.status != 200:
                print(f"HTTP ERROR: status = {response.status}")
                continue
            result = response.read().decode("utf-8")
            results.append(result)
            sleep(1)
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_compare', results)
        results = []
        sleep(poll_seconds)

poll()
