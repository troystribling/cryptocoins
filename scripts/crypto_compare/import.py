from datetime import datetime, timedelta
from dateutil.parser import parse

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.crypto_compare.imports import import_coin_snapshot
from cryptocoins.crypto_compare.imports import import_coin_list
from cryptocoins.crypto_compare.imports import import_currency_pairs_history
from cryptocoins.crypto_compare.imports import import_coin_price_history

from cryptocoins.models.imports import Imports

from cryptocoins.utils import setup_logging

logger = setup_logging()

start_date = parse(sys.argv[1]) if len(sys.argv) > 1 else None
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date
bucket_name = sys.argv[3] if len(sys.argv) > 3 else 'gly.fish'


def start_date_from_last_import(path):
    if start_date is not None:
        return start_date

    import_date = Imports.last_import_date_for_path('cryptocoins/cryptocompare/coin_list')
    if import_date is None:
        return datetime.utcnow()


    return import_date + timedelta(days=1)


def end_date_from_start_date():
    if end_date is not None:
        return end_date
    return datetime.utcnow()

if __name__ == "__main__":
    start_date = start_date_from_last_import('cryptocoins/cryptocompare/coin_list')
    end_date = end_date_from_start_date()
    logger.info(f"IMPORTING coin_list {start_date} TO {end_date} FROM {bucket_name}")
    import_coin_list(bucket_name, start_date, end_date)

    start_date = start_date_from_last_import('cryptocoins/cryptocompare/coin_snapshot')
    end_date = end_date_from_start_date()
    logger.info(f"IMPORTING coin_snapshot {start_date} TO {end_date} FROM {bucket_name}")
    import_coin_snapshot(bucket_name, start_date, end_date)

    start_date = start_date_from_last_import('cryptocoins/cryptocompare/top_pairs')
    end_date = end_date_from_start_date()
    logger.info(f"IMPORTING currency_pairs_history {start_date} TO {end_date} FROM {bucket_name}")
    import_currency_pairs_history(bucket_name, start_date, end_date)

    start_date = start_date_from_last_import('cryptocoins/cryptocompare/histoday')
    end_date = end_date_from_start_date()
    logger.info(f"IMPORTING coin_price_history {start_date} TO {end_date} FROM {bucket_name}")
    import_coin_price_history(bucket_name, start_date, end_date)
