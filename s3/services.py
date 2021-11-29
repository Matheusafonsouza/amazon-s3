import os
import logging
import boto3 as boto
from botocore.exceptions import ClientError


class S3:
    def __init__(self):
        self.sdk = boto.client('s3')

    @property
    def buckets(self):
        return self.sdk.list_buckets().get('Buckets')

    def create_bucket(self, name, region=None):
        try:
            if region is None:
                self.sdk.create_bucket(Bucket=name)
            else:
                location = {'LocationConstraint': region}
                self.sdk.create_bucket(
                    Bucket=name,
                    CreateBucketConfiguration=location
                )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_file(self, file, bucket, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file.name)

        try:
            self.sdk.upload_fileobj(file, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
