"""
This module contains classes for working with database
"""

from abc import ABC, abstractmethod
from psycopg import connect
from models import Item, DetailedItem
from decouple import config

DEBUG = True


class ParserDBManagerABC(ABC):
    """
    Abstract class for database managers
    """
    __instance = None

    def __init__(self):
        self._conn = connect(
                dbname=config('DB_NAME'),
                user=config('DB_USER'),
                password=config('DB_PASSWORD'),
                host=config('DB_HOST'),
                port=config('DB_PORT')
        )

        self._cur = self._conn.cursor()
        if DEBUG:
            self._drop_table()
        self.create_table()

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def insert_item(self, item):
        pass

    @abstractmethod
    def get_items(self, order_by, where, reverse: bool = False) -> list:
        pass

    @abstractmethod
    def get_item(self, url: str) -> DetailedItem:
        pass

    @abstractmethod
    def _drop_table(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        self._conn.close()


class CategoryDBManagerABC(ABC):
    __instance = None

    def __init__(self):
        self._conn = connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT')
        )
        self._cur = self._conn.cursor()
        self.create_table()

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def insert_category(self, category: str):
        pass

    @abstractmethod
    def get_categories(self) -> list:
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        self._conn.close()


class VintedCategoryDBManager(CategoryDBManagerABC):
    def __init__(self):
        super().__init__()

    def create_table(self):
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vinted_categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL)
            """
        )
        self._conn.commit()

    def insert_category(self, category: str):
        self._cur.execute(
            """
            INSERT INTO vinted_categories (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            """,
            (category,)
        )
        self._conn.commit()

    def get_categories(self) -> list:
        self._cur.execute(
            """
            SELECT name FROM vinted_categories
            """
        )
        return [category[0] for category in self._cur.fetchall()]


class VintedDBManager(ParserDBManagerABC):

    def _drop_table(self):
        self._cur.execute(
            """
            DROP TABLE IF EXISTS vinted_items
            """
        )
        self._conn.commit()

    def create_table(self):
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vinted_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price FLOAT,
            brand_name VARCHAR(255),
            size VARCHAR(40),
            color VARCHAR(40),
            category VARCHAR(255),
            condition VARCHAR(255),
            market_place VARCHAR(255),
            date_added TIMESTAMP,
            url VARCHAR(255) UNIQUE NOT NULL)
            """
        )
        self._conn.commit()

    def insert_item(self, item):
        self._cur.execute(
            """
            INSERT INTO vinted_items (name, price, brand_name, size, 
            color, category, condition, market_place, date_added, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (url) DO UPDATE SET 
            name = EXCLUDED.name,
            price = EXCLUDED.price,
            brand_name = EXCLUDED.brand_name,
            size = EXCLUDED.size,
            color = EXCLUDED.color,
            category = EXCLUDED.category,
            condition = EXCLUDED.condition,
            market_place = EXCLUDED.market_place,
            date_added = EXCLUDED.date_added
            """,
            (item.name, item.price, item.brand_name, item.size, item.color,
             item.category, item.condition, item.market_place,
             item.date_added, item.url)
        )
        self._conn.commit()

    def get_items(self, order_by: str = 'id',
                  reverse: bool = False) -> list:
        """
        Gets all items from DB
        :param order_by: Takes name of column to order by
        :param reverse: If True, orders by DESC, else by ASC
        :return: list of items
        """
        if reverse:
            order_by = f'{order_by} DESC'
        else:
            order_by = f'{order_by} ASC'

        self._cur.execute(
            """
            SELECT * FROM vinted_items
            ORDER BY %s
            """, (order_by,)
        )
        return self._cur.fetchall()

    def get_item(self, url: str) -> Item:
        """
        Gets item from DB by url
        :param url: url of item
        :return: Item
        """
        self._cur.execute(
            """
            SELECT * FROM vinted_items
            WHERE url = %s
            """,
            (url,)
        )
        return self._cur.fetchone()


class GrailedDBManager(ParserDBManagerABC):

    def _drop_table(self):
        self._cur.execute(
            """
            DROP TABLE IF EXISTS grailed_items
            """
        )
        self._conn.commit()

    def create_table(self):
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS grailed_items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price FLOAT,
            brand_name VARCHAR(255),
            size VARCHAR(40),
            color VARCHAR(40),
            category VARCHAR(255),
            condition VARCHAR(255),
            market_place VARCHAR(255),
            date_added TIMESTAMP,
            url VARCHAR(255) UNIQUE NOT NULL)
            """
        )
        self._conn.commit()

    def insert_item(self, item):
        self._cur.execute(
            """
            INSERT INTO grailed_items (name, price, brand_name, size, 
            color, category, condition, market_place, date_added, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (url) DO UPDATE SET 
            name = EXCLUDED.name,
            price = EXCLUDED.price,
            brand_name = EXCLUDED.brand_name,
            size = EXCLUDED.size,
            color = EXCLUDED.color,
            category = EXCLUDED.category,
            condition = EXCLUDED.condition,
            market_place = EXCLUDED.market_place,
            date_added = EXCLUDED.date_added
            """,
            (item.name, item.price, item.brand_name, item.size, item.color,
             item.category, item.condition, item.market_place,
             item.date_added, item.url)
        )
        self._conn.commit()

    def get_items(self, order_by: str = 'id',
                  reverse: bool = False) -> list:
        """
        Gets all items from DB
        :param order_by: Takes name of column to order by
        :param reverse: If True, orders by DESC, else by ASC
        :return: list of items
        """
        if reverse:
            order_by = f'{order_by} DESC'
        else:
            order_by = f'{order_by} ASC'

        self._cur.execute(
            """
            SELECT * FROM grailed_items
            ORDER BY %s
            """, (order_by,)
        )
        return self._cur.fetchall()

    def get_item(self, url: str) -> Item:
        """
        Gets item from DB by url
        :param url: url of item
        :return: Item
        """
        self._cur.execute(
            """
            SELECT * FROM grailed_items
            WHERE url = %s
            """,
            (url,)
        )
        return self._cur.fetchone()