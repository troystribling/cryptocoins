# %%
%reload_ext autoreload
%autoreload 2

%aimport tempfile
%aimport os

from cryptocoins import import_data

bucket_name = 'gly.fish'
tempdir = tempfile.gettempdir()

# %%
# fetch cryptocompare coin_list
remote_dir = 'cryptocoins/cryptocompare/coin_list'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_list')
date_dir = '20170708'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))
# list coins
data[0]['Data'].keys()

# %%
# fetch cryptocompare coin_compare
remote_dir = 'cryptocoins/cryptocompare/coin_compare'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_compare')
date_dir = '20170708'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))
len(data)
data[0]['Data']

# %%
# fetch poloniex ticker
remote_dir = 'cryptocoins/poloniex/ticker'
local_dir = os.path.join(tempdir, 'poloniex/ticker')
date_dir = '20170707'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))
len(data)

# %%
# fetch poloniex volume
remote_dir = 'cryptocoins/poloniex/volume'
local_dir = os.path.join(tempdir, 'poloniex/volume')
date_dir = '20170707'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))
data[0].keys()

# %%
# fetch poloniex trades
remote_dir = 'cryptocoins/poloniex/trades'
local_dir = os.path.join(tempdir, 'poloniex/trades')
date_dir = '20170708'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))

# %%
# fetch poloniex book
remote_dir = 'cryptocoins/poloniex/book'
local_dir = os.path.join(tempdir, 'poloniex/book')
date_dir = '20170707'
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=date_dir, end_date=date_dir)
files = os.listdir(os.path.join(local_dir, date_dir))
data = import_data.read_from_file(os.path.join(local_dir, date_dir, files[0]))
data[1]