import sys
from datetime import date
from dateutil.parser import parse

from cryptocoins.crypto_compare.download import download_coin_snapshot
from cryptocoins.crypto_compare.export import request_coin_snapshot
from cryptocoins.crypto_compare.export import request_coin_price_history
from cryptocoins.crypto_compare.export import request_top_currency_pairs


start_date = parse(sys.argv[1]) if len(sys.argv) else date.today()
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")


import_coin_snapshot()
import_coin_list()
import_currency_pairs_history()
import_coin_price_history()
