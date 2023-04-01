from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from ..settings import DEBUG
from .models import Category

Base = declarative_base()


class ParserDbClientABC(ABC):
    """
    Abstract class for database managers
    """
    __instance = None

    def __init__(self):
        self._engine = create_engine(
            f"postgresql://"
            f"{config('DB_USER')}:{config('DB_PASSWORD')}@"
            f"{config('DB_HOST')}:{config('DB_PORT')}/"
            f"{config('DB_NAME')}",
            pool_size=10,  # Set a maximum number of concurrent connections to the database
            max_overflow=20,  # Allow up to 20 additional connections to be created if needed
        )

        Base.metadata.create_all(self._engine)

        self._session_factory = scoped_session(
            sessionmaker(bind=self._engine),
            scopefunc=self._get_scopefunc(),
        )

        if DEBUG:
            try:
                self.clear_table()
            except ProgrammingError:
                self._create_table()

    def _get_scopefunc(self):
        """
        Get a scopefunc to be used with the scoped session. This ensures that each thread gets its own session.
        """
        return None

    @abstractmethod
    def _create_table(self):
        pass

    @abstractmethod
    def clear_table(self):
        pass

    @abstractmethod
    def insert_items(self, items):
        """
        Inserts item to database
        :param items:
        """
        return

    def _initialize_session(self):
        self._session = self._session_factory()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        if hasattr(self, '_session_factory'):
            self._session_factory.remove()
