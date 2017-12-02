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
local_dir = os.path.join(tempdir, remote_dir)
folder_date = parse('20171125')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
coin_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))

# %%
# fetch cryptocompare coin_snapshot
remote_dir = 'cryptocoins/cryptocompare/coin_snapshot'
local_dir = os.path.join(tempdir, remote_dir)
folder_date = parse('20171125')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
compare_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
data = compare_data[0]['Data']['Exchanges']

# %%
# fetch cryptocompare top_pairs
remote_dir = 'cryptocoins/cryptocompare/top_pairs'
local_dir = os.path.join(tempdir, remote_dir)
folder_date = parse('20171126')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
compare_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
data = compare_data[0]['Data']

# %%
# fetch cryptocompare histoday
remote_dir = 'cryptocoins/cryptocompare/histoday'
local_dir = os.path.join(tempdir, remote_dir)
folder_date = parse('20171126')
day_dir = utils.day_dir(folder_date)
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, day_dir))
compare_data = import_data.read_from_file(os.path.join(local_dir, day_dir, files[0]))
data = compare_data[0]