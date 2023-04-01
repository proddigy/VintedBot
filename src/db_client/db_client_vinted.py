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
        try:
            Category.__table__.create(self._engine)
        except ProgrammingError:
            pass

    @property
    def unique_ids(self) -> set[int]:
        unique_ids = self._session.query(VintedItem.unique_id).all()
        return {unique_id[0] for unique_id in unique_ids}

    def get_unpublished_items(self, user_id: int) -> list[Item]:
        """
        Returns a list of unpublished items from the database for the given user.
        :param user_id: int, user ID
        :return: list of Dataclass Item
        """
        user_categories_subquery = select(usercategory.category_id).filter_by(user_id=user_id)
        published_items_subquery = select(userpublisheditem.item_id).filter_by(user_id=user_id)

        unpublished_items = (
            self._session.query(vinteditem)
            .filter(
                vinteditem.category_id.in_(user_categories_subquery),
                vinteditem.unique_id.notin_(published_items_subquery),
            )
            .all()
        )
        return [item(**item.as_dict()) for item in unpublished_items]

    def get_category_name(self, category_id: int) -> str:
        """
        returns the category name for the given category id.
        :param category_id: int, category id
        :return: str, category name
        """
        category = self._session.query(Category).filter(Category.id == category_id).one()
        return category.name

    @property
    def category_ids(self) -> set[int]:
        """
        Returns set of category IDs from the database
        :return: set[int]
        """
        category_ids = self._session.query(Category.id).all()
        return {category_id[0] for category_id in category_ids}

    def get_user_categories(self, user_id: int) -> list[str]:
        user_categories = (
            self._session.query(UserCategory)
            .filter(UserCategory.user_id == user_id)
            .all()
        )
        return [self.get_category_name(category.category_id) for category in user_categories]
