import os
import boto3
import json
import tempfile
import logging
import shutil

from subprocess import call
from datetime import datetime

import cryptocoins.utils as utils
from .models.imports import Imports


logger = logging.getLogger(__name__)


def download_from_s3_to_files(bucket, remote_dir, local_dir, download_limit=None, start_date=None, end_date=None):
    if start_date is None:
        start_date = datetime.utcnow()

    if end_date is None:
        end_date = start_date

    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    logger.info(f"DOWNLOADING FILES IN DATE RANGE {utils.day_dir(start_date)} TO {utils.day_dir(end_date)}")

    downloaded_file_count = 0
    for day in utils.daterange(start_date, end_date):
        day_dir = utils.day_dir(day)
        remote_day_dir = f"{remote_dir}/{day_dir}"
        local_day_dir = f"{local_dir}/{day_dir}"
        if os.path.exists(local_day_dir):
            continue
        os.makedirs(local_day_dir)
        remote_objects = s3_resource.Bucket(bucket).objects.filter(Prefix=remote_day_dir)
        logger.info(f"DOWNLOADING FILES WITH REMOTE PATH {remote_day_dir} TO {local_day_dir}")
        for remote_object in remote_objects:
            downloaded_file_count += 1
            remote_file_name = remote_object.key
            local_file_name = f"{local_day_dir}/{os.path.basename(remote_file_name)}"
            with open(local_file_name, 'wb') as local_file:
                s3_client.download_fileobj(bucket, remote_file_name, local_file)
            call(f'lzop -d {local_file_name}', shell=True)
            os.unlink(local_file_name)
            if download_limit is not None and downloaded_file_count >= download_limit:
                break
        logger.info(f"DOWNLOADED {downloaded_file_count} FILES FROM {remote_day_dir} TO {local_day_dir}")
    logger.info(f'DOWNLOADED {downloaded_file_count} FILES FROM {remote_dir} TO {local_dir}')


def read_from_file(file_name):
    items = []
    with open(file_name, 'r') as file:
        for line in file:
            try:
                json_line = json.loads(line)
            except ValueError:
                logger.error(f"FAILED TO PARSE JSON: {line}")
                break
            else:
                items.append(json_line)
    return items


def import_from_s3(remote_dir):
    def decorator(process):
        def wrapper(bucket_name, start_date, end_date):
            tempdir = tempfile.gettempdir()
            local_dir = os.path.join(tempdir, remote_dir)
            download_from_s3_to_files(bucket_name, remote_dir, local_dir, start_date=start_date, end_date=end_date)
            for day in utils.daterange(start_date, end_date):
                day_dir = utils.day_dir(day)
                data_files = os.listdir(os.path.join(local_dir, day_dir))
                for data_file in data_files:
                    data_file_path = os.path.join(local_dir, day_dir, data_file)
                    if Imports.create_import(remote_dir=remote_dir, date_dir=day_dir, file_name=data_file) is None:
                        continue
                    data = read_from_file(data_file_path)
                    process(data)
            shutil.rmtree(local_dir, ignore_errors=True)
        return wrapper
    return decorator
