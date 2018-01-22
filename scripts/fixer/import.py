from datetime import datetime, timedelta
from dateutil.parser import parse

import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.fixer.imports import import_exchange_rates
from cryptocoins.models.imports import Imports
from cryptocoins.utils import setup_logging


start_date = parse(sys.argv[1]) if len(sys.argv) > 1 else None
end_date = parse(sys.argv[2]) if len(sys.argv) > 2 else start_date
bucket_name = sys.argv[3] if len(sys.argv) > 3 else 'gly.fish'

logger = setup_logging()


def start_date_from_last_import(path):
    if start_date is not None:
        return start_date
    import_date = Imports.last_import_date_for_path(path)
    if import_date is None:
        return datetime.utcnow()
    return import_date + timedelta(days=1)


def end_date_from_start_date():
    if end_date is not None:
        return end_date
    return datetime.utcnow()


if __name__ == "__main__":
    start_date = start_date_from_last_import('forex/fixer/exchange_rates')
    end_date = end_date_from_start_date()
    logger.info(f"IMPORTING fixer/exchange_rates {start_date} TO {end_date} FROM {bucket_name}")
    import_exchange_rates(bucket_name, start_date, end_date)
