import sys
import os
from datetime import date

from dateutil.parser import parse

from cryptocoins.import_data import import_from_s3
from cryptocoins.models.exchanges import Exchanges
from cryptocoins.models.currency_pairs import CurrencyPairs

start_date = date.today()
if len(sys.argv) > 1:
    start_date = parse(sys.argv[1])

end_date = start_date
if len(sys.argv) > 2:
    end_date = parse(sys.argv[2])

print(f"IMPORTING {start_date} to {end_date}")

bucket_name = 'gly.fish'

@import_from_s3(bucket_name, start_date, end_date, 'cryptocoins/cryptocompare/coin_snapshot_full')
def import_coin_snapshot_full(data):
    if len(data) == 0:
        print("ERROR: FILE IS EMPTY")
        return
    if 'Data' not in data[0]:
        print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
        return
    if 'Subs' not in data[0]['Data']:
        print("ERROR: Subs KEY IS MISSING FROM import_coin_snapshot_full")
        return
    for subscription in data[0]['Data']['Subs']:
        print(f"SUBSCRIPTION: {subscription}")
        Exchanges.create_using_cryptocompare_subscription(subscription)
        CurrencyPairs.create_using_cryptocompare_subscription(subscription)

import_coin_snapshot_full()
