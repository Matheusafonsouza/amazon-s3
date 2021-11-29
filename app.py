from s3.services import S3

if __name__ == '__main__':
    s3_client = S3()

    # This is for create a bucket
    # s3_client.create_bucket('afonsotest123')

    # This is for list buckets
    print(s3_client.buckets)
