import boto3
from botocore.errorfactory import ClientError
import json
import pprint

from . import CONFIG_OBJ
from . import LOGGER


class S3Service(object):
    def __init__(self, bucket_name=CONFIG_OBJ.general.s3_bucket_name):
        """Class to interact with S3."""
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

        self.bucket = self.s3_resource.Bucket(bucket_name)

        LOGGER.info('Connected to S3 bucket %s', bucket_name)

    def list(self, last_modified=True):
        if not last_modified:
            ds_bucket_files = [object.key for object in self.bucket.objects.all()]
            return ds_bucket_files
        else:
            ds_bucket_files = [(object.last_modified, object.key) for object in self.bucket.objects.all()]
            sorted_by_time = sorted(ds_bucket_files, key=lambda tupl: tupl[0], reverse=True)
            return sorted_by_time

    def exists_in_bucket(self, key):
        try:
            self.s3_client.head_object(Bucket=self.bucket.name, Key=key)
            return True
        except ClientError:
            return False

    def put(self, filepath, key=None, extra_args=None):
        if not key:
            key = filepath
        self.s3_client.upload_file(filepath, self.bucket.name, key, ExtraArgs=extra_args)
        LOGGER.info('Saved {} to S3 as {}'.format(filepath, key))

    def read(self, key, to_json=False):
        obj = self.bucket.Object(key)
        if to_json:
            key_json = json.loads(
                obj.get()['Body'].read().decode("utf-8")
            )
            return key_json
        else:
            return obj.get()['Body'].read()

    def download(self, key):
        self.s3_client.download_file(self.bucket.name, key, key)

    def delete(self, key):
        LOGGER.info("Delete is not implemented in the S3 wrapper.")

    def url(self, key):
        url = self.s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket.name,
                'Key': key
            }
        )
        return url

    def last_modified_among(self, keys_list):
        all_keys = self.list(last_modified=True)
        relevant_keys = [(d, k) for d, k in all_keys if k in keys_list]
        last_modified = relevant_keys[0][0]
        return last_modified


if __name__ == '__main__':
    from . import S3Service
    s = S3Service()

    s.bucket.objects.limit(5)
