from datetime import datetime
from decimal import Decimal

import csv
import sys
import os

wd = os.getcwd()
sys.path.append(wd)

from cryptocoins.models.forex_pairs_history import ForexPairsHistory
from cryptocoins.utils import setup_logging


if len(sys.argv) < 3:
    raise ValueError('Usage: import file_name symbol')

file_path = sys.argv[1]
to_symbol = sys.argv[2]

logger = setup_logging()


if __name__ == "__main__":
    logger.info(f"IMPORTING FROM {file_path}, SYMBOL {to_symbol}")
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i in range(5):
            next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            if not row[1]:
                continue
            timestamp_epoc = datetime.strptime(row[0], '%d/%m/%y').timestamp()
            price_dollars = Decimal(row[1].replace(',', ''))
            model_params = {'from_symbol': 'USD',
                            'to_symbol': to_symbol,
                            'price': Decimal(1.0) / price_dollars,
                            'timestamp_epoc': timestamp_epoc}
            data.append(model_params)
    ForexPairsHistory.create_from_model_params(data)
