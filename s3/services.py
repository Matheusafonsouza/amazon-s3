import os
import logging
import boto3 as boto
from botocore.exceptions import ClientError
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class S3:
    def __init__(self):
        """
        S3 constructor, it will be where we start the sdk instance with the
        credentials from the environment file.
        """
        self.sdk = boto.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    @property
    def buckets(self):
        """
        Return all buckets for this credentiated user.
        :returns: List of buckets or raise a error
        """
        try:
            return self.sdk.list_buckets().get('Buckets')
        except ClientError as e:
            logging.error(e)

    def list_bucket_objects(self, bucket):
        """
        Return all files for a given bucket.
        :param bucket: Bucket name
        :returns: List of objects inside the given bucket
        """
        try:
            return self.sdk.list_objects(Bucket=bucket).get('Contents')
        except ClientError as e:
            logging.error(e)

    def create_bucket(self, name, region=None):
        """
        Create a new bucket with a given name and region, if we give no region,
        it will use the default region for this credentiated user.
        :param name: Name for the bucket
        :param region: Region where the bucket will be created
        :returns: True if created the bucket, false if dont
        """
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

    def upload(self, file_path, bucket, object_name=None):
        """
        Upload a file to a given bucket with a name, if we give no name it will
        use the file basename.
        :param file_path: Path for uploaded file
        :param bucket: Bucket where the file will be uploaded
        :param object_name: File name inside the bucket
        :returns: True if uploaded the file, false if dont
        """
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            with open(file_path, 'rb') as file:
                self.sdk.upload_fileobj(file, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download(self, file_path, bucket, filename):
        """
        Download a file from inside a given bucket.
        :param file_path: Path for downloaded file
        :param bucket: Bucket where the file is in
        :param filename: Name from the file inside the bucket
        """
        try:
            with open(file_path, 'wb') as f:
                self.sdk.download_fileobj(bucket, filename, f)
        except ClientError as e:
            os.remove(file_path)
            logging.error(e)

    def delete_file(self, bucket, filename):
        """
        Deletes a file inside a given bucket.
        :param bucket: Bucket where the file is in
        :param filename: Name from the file inside the bucket
        :returns: True if file was deleted, false if dont
        """
        try:
            self.sdk.delete_object(Bucket=bucket, Key=filename)
        except ClientError as e:
            logging.error(e)
            return False
        return True
