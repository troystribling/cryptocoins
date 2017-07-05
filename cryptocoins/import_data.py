import tempfile
import os
import boto3

from subprocess import call
from datetime import timedelta, date
from dateutil.parser import parse

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

def download_from_s3(bucket, remote_dir, local_dir, start_date=None, end_date=None):
    download_from_s3_to_files(bucket, remote_dir, local_dir=local_dir, start_date=start_date, end_date=end_date)

def download_from_s3_to_files(bucket, remote_dir, local_dir, start_date=None, end_date=None):
    if start_date is None:
        start_date = date.today()
    else:
        start_date = parse(start_date)

    if end_date is None:
        end_date = date.today()
    else:
        end_date = parse(end_date)

    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    for day in daterange(start_date, end_date):
        day_dir = day.strftime('%Y%m%d')
        remote_day_dir = f"{remote_dir}/{day_dir}"
        local_day_dir = f"{local_dir}/{day_dir}"
        if not os.path.exists(local_day_dir):
            os.makedirs(local_day_dir)
        remote_objects = s3_resource.Bucket(bucket).objects.filter(Prefix=remote_day_dir)
        for remote_object in remote_objects:
            remote_file_name = remote_object.key
            local_file_name = f"{local_day_dir}/{os.path.basename(remote_file_name)}"
            print(f'DOWNLOADING: {remote_file_name} to {local_file_name}')
            with open(local_file_name, 'wb') as local_file:
                s3_client.download_fileobj(bucket, remote_file_name, local_file)
            call(f'lzop -d {local_file_name}', shell=True)
