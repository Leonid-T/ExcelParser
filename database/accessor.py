from abc import ABC, abstractmethod
from sqlalchemy import create_engine

from .model import metadata


class DBAccessor(ABC):
    @abstractmethod
    def engine(self):
        pass


class SQLiteAccessor(DBAccessor):
    """
    Accessor to connect to the database
    """
    _engine = None
    _metadata = metadata

    def __init__(self, filepath: str):
        self._engine = create_engine(f"sqlite:///{filepath}")

    @property
    def engine(self):
        return self._engine

    def create_tables(self):
        self._metadata.create_all(self._engine)

    def delete_tables(self):
        self._metadata.drop_all(self._engine)
