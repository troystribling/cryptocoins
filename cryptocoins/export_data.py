import tempfile
import os
import boto3
import requests

from subprocess import call
from datetime import date, datetime

from cryptocoins import utils
from cryptocoins.models.collections import Collections


def upload_to_s3(bucket, path, data):
    local_path = write_to_compressed_file(data)
    upload_file_to_s3(bucket, path, local_path)


def write_to_compressed_file(data):
    file_name_prefix = utils.date_prefix(datetime.utcnow())
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
    remote_object = f"{path}/{utils.day_dir(date.today())}/{os.path.basename(local_path)}"
    bucket.put_object(Key=remote_object, Body=open(local_path, 'rb'))
    os.unlink(local_path)
    print(f'{datetime.now()}: UPLOADED to {remote_object}')


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        print(error)
        return None
    else:
        return response


def fetch_url_and_upload(process):
    def wrapper(collection_name, url, bucket, path):
        print(f"FETCH FROM: {url}")
        if Collections.create_collection(name=collection_name, url=url) is None:
            return
        reult = fetch_url(url)
        if result is not None:
            processed_result = process(result)
            upload_file_to_s3(bucket, path, processed_result)
        else:
            print(f"ERROR: REQUEST FAILED FOR URL {url}")
    return wrapperabs
