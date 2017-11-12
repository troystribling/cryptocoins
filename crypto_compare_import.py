import sys
import os
from datetime import date
import tempfile

from cryptocoins import import_data
from cryptocoins import utils


start_date = utils.day_dir(date.today())
if len(sys.argv) > 1:
    start_date = sys.argv[1]

end_date = start_date
if len(sys.argv) > 2:
    end_date = sys.argv[2]

print(f"IMPORTING {start_date} to {end_date}")

tempdir = tempfile.gettempdir()
bucket_name = 'gly.fish'

remote_dir = 'cryptocoins/cryptocompare/coin_snapshot_full'
local_dir = os.path.join(tempdir, 'cryptocompare/coin_snapshot_full')
import_data.download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=start_date, end_date=end_date)

files = os.listdir(os.path.join(local_dir, start_date))
compare_data = import_data.read_from_file(os.path.join(local_dir, start_date, files[0]))
compare_data[0]['Data']['Subs']
