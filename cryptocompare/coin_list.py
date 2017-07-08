from time import sleep
from urllib.request import urlopen

import sys

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import export_data

poll_seconds = 3600

def poll():
    while True:
        url = 'https://www.cryptocompare.com/api/data/coinlist/'
        response = urlopen(url)
        if response.status != 200:
            print(f"HTTP ERROR: status = {response.status}")
            continue
        result = response.read().decode("utf-8")
        export_data.upload_to_s3('gly.fish', 'cryptocoins/cryptocompare/coin_list', [result])
        sleep(poll_seconds)

poll()
