from time import sleep
from urllib.request import urlopen

import os
import sys
file_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.join(file_path, '..'))

from cryptocoins import export_data

poll_seconds = 86400

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
