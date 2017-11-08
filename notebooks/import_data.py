# %%
import tempfile
import os

from cryptocoins import import_data

bucket_name = 'gly.fish'
tempdir = tempfile.gettempdir()

# %%
# fetch cryptocompare coin_list
remote_dir = 'cryptocoins/cryptocompare/coin_list'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_list')
folder_date = '20170708'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, folder_date))
data = import_data.read_from_file(os.path.join(local_dir, folder_date, files[0]))
# list coins
data[0]['Data'].keys()

# %%
# fetch cryptocompare coin_compare
remote_dir = 'cryptocoins/cryptocompare/coin_compare'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_compare')
folder_date = '20170708'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=folder_date, end_date=folder_date)
files = os.listdir(os.path.join(local_dir, folder_date))
data = import_data.read_from_file(os.path.join(local_dir, folder_date, files[0]))
len(data)
data[0]['Data']
