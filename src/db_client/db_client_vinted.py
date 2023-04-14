"""
This module contains VintedDBManager class
"""
from dataclasses import asdict

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import and_, select

from ..data_structures import Item
from .db_client_abc import ParserDbClientABC
from .models import *


class VintedDbClient(ParserDbClientABC):
    """
    Class for working with database for Vinted
    """

    def __init__(self):
        super().__init__()
        self._reference = 'vinted'
        self._initialize_session()

    def insert_items(self, items: list[Item]):
        dicts = [asdict(item) for item in items]
        stmt = pg_insert(VintedItem).values(dicts).on_conflict_do_nothing()
        self._session.execute(stmt)
        self._session.commit()

    def clear_table(self):
        """
        Clears table
        :return:
        """
        UserPublishedItem.__table__.drop(self._engine, checkfirst=True)
        VintedItem.__table__.drop(self._engine, checkfirst=True)
        self._create_table()

    def _create_table(self):
        VintedItem.__table__.create(self._engine)
        UserPublishedItem.__table__.create(self._engine)
        try:
            Category.__table__.create(self._engine)
        except ProgrammingError:
            pass

    @property
    def unique_ids(self) -> set[int]:
        unique_ids = self._session.query(VintedItem.unique_id).all()
        return {unique_id[0] for unique_id in unique_ids}

    def get_category_name(self, category_id: int) -> str:
        """
        returns the category name for the given category id.
        :param category_id: int, category id
        :return: str, category name
        """
        category = self._session.query(Category).filter(Category.id == category_id).one()
        return category.name

    @property
    def categories(self) -> set[Category]:
        """
        returns all categories
        :return: set[Category], set of all categories
        """
        return set(self._session.query(Category).all())
