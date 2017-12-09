import sys
from datetime import date
from dateutil.parser import parse

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.crypto_compare.imports import import_currency_pairs_history
from cryptocoins.crypto_compare.imports import import_coin_price_history

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")

start_date = parse(sys.argv[1]) if len(sys.argv) else date.today()
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date

print(f"IMPORTING {start_date} TO {end_date} FROM {bucket_name}")

if __name__ == "__main__":
    import_coin_snapshot(start_date, end_date)
    import_coin_list(start_date, end_date)
    import_currency_pairs_history(start_date, end_date)
    import_coin_price_history(start_date, end_date)
