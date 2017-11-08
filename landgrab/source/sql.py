from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from landgrab.source import BaseSource


def _compose_sql_uri(uri, dialect, driver):
    return uri.replace('sql://', '%s+%s://' % (dialect, driver))


def _start_session(sql_uri):
    """
    Starts a session with the database
    """
    engine = create_engine(sql_uri)
    session_factory = sessionmaker()
    session_factory.configure(bind=engine)
    session = session_factory()
    return session


class SQLSource(BaseSource):
    """
    An input source for data stored in a SQL database
    """
    def __init__(self, uri, query, dialect='postgresql', driver='psycopg2'):
        self.uri = uri
        self.query = query
        self.dialect = dialect
        self.driver = driver

    def __enter__(self):
        sql_uri = _compose_sql_uri(self.uri, self.dialect, self.driver)
        sql_session = _start_session(sql_uri)
        self.download_stream = sql_session.execute(self.query)
        return self

    def pull(self):
        return self.download_stream

    def __exit__(self, *args):
        self.download_stream.close()
