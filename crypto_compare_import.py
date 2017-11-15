import sys
import os
from datetime import date
import tempfile

from dateutil.parser import parse

from cryptocoins import import_data
from cryptocoins import utils
from cryptocoins.models.exchanges import Exchanges
from cryptocoins.models.currency_pairs import CurrencyPairs
from cryptocoins.models.imports import Imports

def import_coin_snapshot_full(bucket_name, start_date, end_date):
    remote_dir = 'cryptocoins/cryptocompare/coin_snapshot_full'
    tempdir = tempfile.gettempdir()
    local_dir = os.path.join(tempdir, remote_dir)
    import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=start_date, end_date=end_date)
    for day in utils.daterange(start_date, end_date):
        day_dir = utils.day_dir(day)
        data_files = os.listdir(os.path.join(local_dir, day_dir))
        for data_file in data_files:
            data_file_path = os.path.join(local_dir, day_dir, data_file)
            if Imports.create_import(remote_dir=remote_dir, date_dir=day_dir, file_name=data_file) is None:
                continue
            data = import_data.read_from_file(data_file_path)
            if len(data) == 0:
                print("ERROR: FILE IS EMPTY")
                continue
            if 'Data' not in data[0]:
                print("ERROR: Data KEY IS MISSING FROM import_coin_snapshot_full")
                continue
            if 'Subs' not in data[0]['Data']:
                print("ERROR: Subs KEY IS MISSING FROM import_coin_snapshot_full")
                continue
            for subscription in data[0]['Data']['Subs']:
                print(f"SUBSCRIPTION: {subscription}")
                Exchanges.create_using_cryptocompare_subscription(subscription)
                CurrencyPairs.create_using_cryptocompare_subscription(subscription)


def import_coin_list(bucket_name, start_date, end_date):
    remote_dir = 'cryptocoins/cryptocompare/coin_list'
    tempdir = tempfile.gettempdir()
    local_dir = os.path.join(tempdir, remote_dir)
    import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=start_date, end_date=end_date)
    for day in utils.daterange(start_date, end_date):
        day_dir = utils.day_dir(day)
        data_files = os.listdir(os.path.join(local_dir, day_dir))
        for data_file in data_files:
            data_file_path = os.path.join(local_dir, day_dir, data_file)
            if Imports.create_import(remote_dir=remote_dir, date_dir=day_dir, file_name=data_file) is None:
                continue
            data = import_data.read_from_file(data_file_path)


if __name__ == "__main__":

    start_date = date.today()
    if len(sys.argv) > 1:
        start_date = parse(sys.argv[1])

    end_date = start_date
    if len(sys.argv) > 2:
        end_date = parse(sys.argv[2])

    bucket_name = 'gly.fish'

    print(f"IMPORTING {start_date} to {end_date}")

    import_coin_snapshot_full(bucket_name, start_date, end_date)
