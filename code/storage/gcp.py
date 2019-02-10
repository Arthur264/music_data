from google.cloud import storage


class BucketClient:
    bucket = None

    def __init__(self, bucket_name):
        self.bucket = self.create_bucket(bucket_name)

    @staticmethod
    def create_bucket(bucket_name):
        storage_client = storage.Client()
        return storage_client.get_bucket(bucket_name)
