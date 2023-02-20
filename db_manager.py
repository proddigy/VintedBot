import os
from abc import ABC, abstractmethod
from psycopg import connect
from models import Item


DEBUG = True


class ParserDBManagerABC(ABC):
    __instance = None

    def __init__(self):
        try:
            self._conn = connect(
                dbname=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                host=os.environ['DB_HOST'],
                port=os.environ['DB_PORT']
            )
        except Exception as e:
            print(e)
            exit()
        self._cur = self._conn.cursor()
        if DEBUG:
            self.drop_table()
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
    def get_item(self, url: str) -> Item:
        pass

    @abstractmethod
    def drop_table(self):
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
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
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
    def __init__(self):
        super().__init__()

    def drop_table(self):
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
            url VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255),
            price FLOAT,
            brand_name VARCHAR(255),
            size VARCHAR(40),
            color VARCHAR(40),
            category VARCHAR(255),
            description TEXT,
            condition VARCHAR(255),
            shipping VARCHAR(255),
            seller VARCHAR(255),
            market_place VARCHAR(255),
            date_added TIMESTAMP)
            """
        )
        self._conn.commit()

    def insert_item(self, item):
        self._cur.execute(
            """
            INSERT INTO vinted_items (url, name, price, brand_name, size, color, category, description, condition, shipping, seller)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (url) DO UPDATE SET 
            name = EXCLUDED.name,
            price = EXCLUDED.price,
            brand_name = EXCLUDED.brand_name,
            size = EXCLUDED.size,
            color = EXCLUDED.color,
            category = EXCLUDED.category,
            description = EXCLUDED.description,
            condition = EXCLUDED.condition,
            shipping = EXCLUDED.shipping,
            seller = EXCLUDED.seller
            """,
            (item.url, item.name, item.price, item.brand_name, item.size, item.color, item.category, item.description,
             item.condition, item.shipping, item.seller)
        )
        self._conn.commit()

    def get_items(self, order_by, where, reverse: bool = False) -> list:
        """
        Gets all items from DB
        :param order_by: Takes name of column to order by
        :param where: Takes name of column to filter by
        :param reverse: If True, orders by DESC, else by ASC
        :return: list of items
        """
        if reverse:
            order_by = f'{order_by} DESC'
        else:
            order_by = f'{order_by} ASC'

        if where:
            where = f'WHERE {where}'
        else:
            where = ''

        self._cur.execute(
            """
            SELECT * FROM vinted_items
            %s
            ORDER BY %s
            """, (where, order_by)
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
            SELECT * FROM Vinted.items
            WHERE url = %s
            """,
            (url,)
        )
        return self._cur.fetchone()
