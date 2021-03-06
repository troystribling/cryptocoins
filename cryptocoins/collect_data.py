import tempfile
import os
import boto3
import requests
import logging

from subprocess import call
from datetime import datetime

from cryptocoins import utils
from cryptocoins.models.collections import Collections


logger = logging.getLogger(__name__)


def upload_to_s3(bucket_name, path, data):
    local_path = write_to_compressed_file(data)
    upload_file_to_s3(bucket_name, path, local_path)


def write_to_compressed_file(data):
    file_name_prefix = utils.date_prefix(datetime.utcnow())
    file = tempfile.NamedTemporaryFile(delete=False, mode='w', prefix=file_name_prefix)
    for data_item in data:
        print(data_item, file=file)
    file.close()
    call(f'lzop {file.name}', shell=True)
    os.unlink(file.name)
    return f'{file.name}.lzo'


def upload_file_to_s3(bucket_name, path, local_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    remote_object = f"{path}/{utils.day_dir(datetime.utcnow())}/{os.path.basename(local_path)}"
    bucket.put_object(Key=remote_object, Body=open(local_path, 'rb'))
    os.unlink(local_path)
    logger.info(f'{datetime.now()}: UPLOADED TO {bucket_name}/{remote_object}')


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        logger.error(error)
        return None
    else:
        return response


def fetch_url_and_upload_to_s3(process):
    def wrapper(**params):
        logger.info(f"FETCH FROM: {params['url']}")
        meta = params['meta'] if 'meta' in params else None
        collection = Collections.create_collection(path=params['path'], url=params['url'], meta=meta)
        if collection is None:
            logger.error(f"Collection with {params['url']} exists")
            return
        response = fetch_url(params['url'])
        if response is not None:
            params['response'] = response
            processed_response = process(params)
            upload_to_s3(bucket_name=params['bucket_name'], path=params['path'], data=processed_response)
            collection.collection_successful()
        else:
            logger.error(f"REQUEST FAILED FOR URL {params['url']}")
    return wrapper
