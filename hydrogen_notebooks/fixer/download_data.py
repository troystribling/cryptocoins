# %%
import tempfile
import os
from dateutil.parser import parse

from cryptocoins import import_data
from cryptocoins import utils
from cryptocoins.utils import setup_logging

bucket_name = 'gly.fish.dev'
logger = setup_logging()
tempdir = tempfile.gettempdir()

# %%
# fetch cryptocompare coin_list, coins
remote_dir = 'forex/fixer/exchange_rates'
local_dir = os.path.join(tempdir, remote_dir)
folder_date = parse('20180122')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
coin_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
coins = coin_data[0]['Data']
len(coins)
