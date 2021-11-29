from s3.services import S3

if __name__ == '__main__':
    s3_client = S3()

    # This is for create a bucket
    s3_client.create_bucket('afonsotest123')

    # This is for upload file inside  a bucket
    s3_client.upload('./files/example.txt', 'afonsotest123', 'cool.txt')

    # This is for download a file
    s3_client.download('./downloads/cool.txt',
                       'afonsotest123', 'testelegal.txt')

    # This is for list objects of bucket
    objects = s3_client.list_bucket_objects('afonsotest123')
    print(objects)

    # This is for list objects of bucket
    s3_client.delete_file('afonsotest123', 'testelegal.txt')

    # This is for list buckets
    print(s3_client.buckets)
