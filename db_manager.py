from psycopg import connect
from abc import ABC, abstractmethod
from models import Item
from decouple import config


class DBManagerABC(ABC):
    def __init__(self):
        self._conn = connect(
            dbname=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            port=config('DB_PORT')
        )
        self._cur = self._conn.cursor()

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


class VintedDBManager(DBManagerABC):
    def __init__(self):
        super().__init__()
        self.__market_place = 'Vinted'

    def create_table(self):
        self._cur.execute(
            """
            CREATE TABLE IF NOT EXISTS %s.items (
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
            """, (self.__market_place,)
        )
        self._conn.commit()

    def insert_item(self, item):
        self._cur.execute(
            """
            INSERT INTO Vinted.items (url, name, price, brand_name, size, color, category, description, condition, shipping, seller)
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
            SELECT * FROM Vinted.items
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

    def __del__(self):
        self._conn.close()
