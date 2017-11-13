# %%
import tempfile
import os
from dateutil.parser import parse

from cryptocoins import import_data
from cryptocoins import utils


bucket_name = 'gly.fish'
tempdir = tempfile.gettempdir()

# %%
# fetch cryptocompare coin_list
remote_dir = 'cryptocoins/cryptocompare/coin_list'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_list')
folder_date = parse('20171111')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
coin_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
# list coins
coin_data[0]['Data']['ETH']

# %%
# fetch cryptocompare coin_compare
remote_dir = 'cryptocoins/cryptocompare/coin_snapshot_full'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_snapshot_full')
folder_date = parse('20171113')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
compare_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
sub = compare_data[0]['Data']['Subs'][0]
