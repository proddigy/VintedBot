"""
This module contains VintedDBManager class
"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text,\
    insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.data_structures import Item
from src.db_client.db_client_abc import ParserDbClientABC
from dataclasses import asdict
from decouple import config
from src.settings import DEBUG

Base = declarative_base()


class VintedItem(Base):
    __tablename__ = 'vinted_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    unique_id = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    brand_name = Column(String(255), nullable=False)
    size = Column(String(10), nullable=False)
    url = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=False)


class VintedDbClient(ParserDbClientABC):
    """
    Class for working with database for Vinted
    """

    def __init__(self):
        super().__init__()
        self._reference = 'vinted'

    def insert_items(self, items: list[Item]):
        """
        Batch inserts items to database
        :param items: list of Dataclass Item
        :return: no return
        """
        dicts = [asdict(item) for item in items]
        stmt = insert(VintedItem).values(dicts)
        self._session.execute(stmt)
        self._session.commit()

    def _drop_table(self):
        VintedItem.__table__.drop(self._engine)

    def _create_table(self):
        VintedItem.__table__.create(self._engine)

    def get_unique_ids(self) -> set[int]:
        """
        Returns set of unique ids from database
        :return: set[int]
        """
        unique_ids = self._session.query(VintedItem.unique_id).all()
        return {unique_id[0] for unique_id in unique_ids}
