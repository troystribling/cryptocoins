import tempfile
import os
import boto3
import sys
import requests

from subprocess import call
from datetime import date, datetime


def upload_to_s3(bucket, path, data):
    local_path = write_to_compressed_file(data)
    upload_file_to_s3(bucket, path, local_path)


def write_to_compressed_file(data):
    file_name_prefix = datetime.utcnow().strftime('%Y%m%d-%H%M%S-')
    file = tempfile.NamedTemporaryFile(delete=False, mode='w', prefix=file_name_prefix)
    for data_item in data:
        print(data_item, file=file)
    file.close()
    call(f'lzop {file.name}', shell=True)
    os.unlink(file.name)
    return f'{file.name}.lzo'


def upload_file_to_s3(bucket, path, local_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    remote_object = f"{path}/{date.today().strftime('%Y%m%d')}/{os.path.basename(local_path)}"
    bucket.put_object(Key=remote_object, Body=open(local_path, 'rb'))
    os.unlink(local_path)
    print(f'{datetime.now()}: UPLOADED to {remote_object}')


def getURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        print(sys.exc_info())
        return None
    else:
        return response
