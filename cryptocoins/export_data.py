import tempfile
import os
import boto3

from subprocess import call
from datetime import date

def upload_to_s3(bucket, path, data):
    local_path = write_to_compressed_file(data)
    upload_file_to_s3(bucket, path, local_path)

def write_to_compressed_file(data):
    file = tempfile.NamedTemporaryFile(delete=False, mode='w')
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
