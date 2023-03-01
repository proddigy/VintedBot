"""
This module contains classes for working with database
"""
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from src.settings import DEBUG


Base = declarative_base()


class ParserDbClientABC(ABC):
    """
    Abstract class for database managers
    """
    __instance = None

    def __init__(self):
        self._engine = create_engine(
            f"postgresql://"
            f"{config('DB_USER')}:"
            f"{config('DB_PASSWORD')}@"
            f"{config('DB_HOST')}:"
            f"{config('DB_PORT')}/"
            f"{config('DB_NAME')}"
        )

        Base.metadata.create_all(self._engine)

        Session_SQL = sessionmaker(bind=self._engine)
        self._session = Session_SQL()

        if DEBUG:
            self._drop_table()

    @abstractmethod
    def _create_table(self):
        pass

    @abstractmethod
    def _drop_table(self):
        pass

    @abstractmethod
    def insert_items(self, item):
        """
        Inserts item to database
        :param item:
        """
        return

    @abstractmethod
    def get_unique_ids(self) -> set[int]:
        """
        Returns set of unique ids from database
        :return: set[int]
        """
        unique_ids = self._session.query(Table_name.unique_id).all()
        return {unique_id[0] for unique_id in unique_ids}

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        self._session.close_all()
