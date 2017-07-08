from time import sleep
from urllib.request import urlopen

import sys

if '../cryptocoins' not in sys.path:
    sys.path.append('../cryptocoins')

from cryptocoins import export_data

results_per_file = 150
poll_seconds = 60.0

def poll():
    total_results_count = 0
    results = []
    while True:
        total_results_count += 1
        url = 'https://poloniex.com/public?command=return24hVolume'
        response = urlopen(url)
        if response.status != 200:
            print(f"HTTP ERROR: status = {response.status}")
            continue
        result = response.read().decode("utf-8")
        results.append(result)
        if total_results_count % results_per_file == 0:
            export_data.upload_to_s3('gly.fish', 'cryptocoins/poloniex/volume', results)
            results = []
        sleep(poll_seconds)

poll()
