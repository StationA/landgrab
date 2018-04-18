import shutil
import smart_open
import tempfile
from urllib.parse import unquote_plus, urlsplit


from landgrab.source import BaseSource


def _parse_uri(uri):
    """
    Parses an S3 URI
    """
    parts = urlsplit(uri)
    netloc = parts.hostname
    path = unquote_plus(parts.path[1:])
    username = unquote_plus(parts.username) if parts.username else None
    password = unquote_plus(parts.password) if parts.password else None
    return username, password, netloc, path


def _compose_uri(access_key_id, secret_access_key, bucket, key):
    """
    Creates an S3 URI from the required fields; the inverse operation of `_parse_uri`
    """
    return 's3://%s:%s@%s/%s' % (access_key_id, secret_access_key, bucket, key)


class S3Source(BaseSource):
    """
    An input source for data blobs stored in S3
    """
    # TODO: Support glob URIs?
    def __init__(self, uri, access_key_id=None, secret_access_key=None):
        username, password, bucket, key = _parse_uri(uri)
        self.access_key_id = access_key_id if access_key_id else username
        self.secret_access_key = secret_access_key if secret_access_key else password
        self.bucket = bucket
        self.key = key

    def __enter__(self):
        s3_uri = _compose_uri(self.access_key_id, self.secret_access_key, self.bucket, self.key)
        self.f = tempfile.NamedTemporaryFile(delete=True)
        self.download_stream = smart_open.smart_open(s3_uri, mode='rb')
        return self

    def pull(self):
        shutil.copyfileobj(self.download_stream, self.f)
        self.f.flush()
        self.f.seek(0)
        return self.f

    def __exit__(self, *args):
        self.f.close()
