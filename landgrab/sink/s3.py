import boto3
from StringIO import StringIO
import urlparse
import urllib


from landgrab.sink import BaseSink


def _parse_uri(uri):
    """
    Parses an S3 URI
    """
    parts = urlparse.urlsplit(uri)
    netloc = parts.hostname
    path = urllib.unquote_plus(parts.path[1:])
    username = urllib.unquote_plus(parts.username) if parts.username else None
    password = urllib.unquote_plus(parts.password) if parts.password else None
    return username, password, netloc, path


def _create_client(access_key_id, secret_access_key):
    """
    Creates a boto3 s3 client
    """
    client = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    return client


class S3Sink(BaseSink):
    def __init__(self, uri, access_key_id=None, secret_access_key=None):
        username, password, bucket, key = _parse_uri(uri)
        self.access_key_id = access_key_id if access_key_id else username
        self.secret_access_key = secret_access_key if secret_access_key else password
        self.bucket = bucket
        self.key = key

    def __enter__(self):
        self.client = _create_client(self.access_key_id, self.secret_access_key)
        self.upload_buf = StringIO()
        return self

    def save(self, item):
        self.upload_buf.write(item)

    def __exit__(self, *args):
        self.upload_buf.seek(0)
        self.client.upload_fileobj(self.upload_buf, self.bucket, self.key)
