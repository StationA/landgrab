import smart_open
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


def _compose_uri(access_key_id, secret_access_key, bucket, key):
    return 's3://%s:%s@%s/%s' % (access_key_id, secret_access_key, bucket, key)


class S3Sink(BaseSink):
    def __init__(self, uri, access_key_id=None, secret_access_key=None):
        username, password, bucket, key = _parse_uri(uri)
        self.access_key_id = access_key_id if access_key_id else username
        self.secret_access_key = secret_access_key if secret_access_key else password
        self.bucket = bucket
        self.key = key

    def __enter__(self):
        s3_uri = _compose_uri(self.access_key_id, self.secret_access_key, self.bucket, self.key)
        self.upload_stream = smart_open.smart_open(s3_uri, mode='wb')
        return self

    def save(self, item):
        self.upload_stream.write(item)

    def __exit__(self, *args):
        self.upload_stream.close()
