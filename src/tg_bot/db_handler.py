import asyncio
from typing import List
from aiogram import types
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from decouple import config
from typing import Optional
from src.db_client.models import *
from src.logger import logger

db_config = f"postgresql+asyncpg://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}/{config('DB_NAME')}"


class SessionManager:
    def __init__(self, db_config: str):
        self.async_engine = create_async_engine(db_config)
        self.sync_engine = create_sync_engine(db_config.replace("postgresql+asyncpg", "postgresql"))
        self.async_session = None

    async def init_async_session(self):
        if self.async_session is not None:
            raise RuntimeError("Async session already initialized")
        self.async_session = sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)
        logger.info('Async session initialized')

    async def close_async_session(self):
        if self.async_session is not None:
            await self.async_session.close()
            logger.info('Async session closed')
        self.async_session = None

    def get_sync_session(self):
        return sessionmaker(self.sync_engine)()


session_manager = SessionManager(db_config)


async def init_engine():
    await session_manager.init_async_session()
    Base.metadata.create_all(session_manager.sync_engine, checkfirst=True)
    logger.info('Database schema initialized')


@asynccontextmanager
async def get_session() -> AsyncSession:
    if session_manager.async_session is None:
        await init_engine()

    async with session_manager.async_session() as session:
        try:
            logger.info("Async session successfully connected")
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


async def create_user(user: types.User) -> None:
    async with get_session() as session:
        try:
            user = TelegramBotUser(id=user.id, username=user.username, first_name=user.first_name, active=True)
            session.add(user)
        except Exception as e:
            logger.error(e)
            raise


async def is_active(user: types.User) -> bool:
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.id == user.id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user is not None and user.active


async def get_all_active_users():
    """
    Returns ids of all active users
    :return: list[user.id]
    """
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.active)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return [user.id for user in users]


async def is_admin_async(user_id: int) -> bool:
    async with get_session() as session:
        stmt = select(AdminUser).where(AdminUser.user_id == user_id)
        result = await session.execute(stmt)
        admin_user = result.scalars().first()
        return admin_user is not None and admin_user.is_admin


async def activate_user_by_id_async(user_id: int) -> None:
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user:
            user.active = True
            await session.commit()


async def deactivate_user_by_id_async(user_id: int) -> None:
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user:
            user.active = False
            await session.commit()


async def get_user_by_username_async(username: str) -> Optional[TelegramBotUser]:
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.username == username)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user


async def get_user_by_id_async(user_id: int) -> Optional[TelegramBotUser]:
    async with get_session() as session:
        stmt = select(TelegramBotUser).where(TelegramBotUser.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user


async def get_admin_users_ids() -> List[int]:
    async with get_session() as session:
        stmt = select(AdminUser).where(AdminUser.is_admin == True)
        result = await session.execute(stmt)
        admin_ids = result.scalars().all()
        admin_ids = list(map(lambda x: x.user_id, admin_ids))
        return admin_ids


async def get_unpublished_items(user_id: int) -> List[VintedItem]:
    async with get_session() as session:
        stmt = (
            select(VintedItem)
            .where(
                VintedItem.id.notin_(
                    select(UserPublishedItem.item_id).where(UserPublishedItem.user_id == user_id)
                )
            )
            .order_by(VintedItem.brand_name, VintedItem.price)
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return items


async def add_published_item(user_id: int, item_id: int) -> None:
    async with get_session() as session:
        user_published_item = UserPublishedItem(user_id=user_id, item_id=item_id)
        session.add(user_published_item)


async def get_categories() -> List[Category]:
    async with get_session() as session:
        stmt = select(Category)
        result = await session.execute(stmt)
        categories = result.scalars().all()
        return categories


async def get_user_categories(user_id: int) -> List[Category]:
    async with get_session() as session:
        stmt = select(Category).join(UserCategory).where(UserCategory.user_id == user_id)
        result = await session.execute(stmt)
        user_categories = result.scalars().all()
        return user_categories


async def clear_table() -> None:
    async with get_session() as session:
        await session.execute(delete(UserPublishedItem))
        await session.execute(delete(Item))
        await session.commit()


async def add_category_to_user(user_id: int, category_id: int):
    async with get_session() as session:
        # Check if the user already has the category
        stmt = select(UserCategory).where(
            (UserCategory.user_id == user_id) & (UserCategory.category_id == category_id)
        )
        result = await session.execute(stmt)
        user_category = result.scalars().first()

        if user_category is None:
            # Create a new UserCategory record if it doesn't exist
            user_category = UserCategory(user_id=user_id, category_id=category_id)
            session.add(user_category)
            await session.commit()


async def create_category(category_name: str) -> Category:
    async with get_session() as session:
        category = Category(name=category_name)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


async def get_unpublished_items_by_category(user_id: int, category_id: int) -> List[VintedItem]:
    async with get_session() as session:
        stmt = (
            select(VintedItem)
            .join(UserPublishedItem, VintedItem.id == UserPublishedItem.item_id, isouter=True)
            .where(VintedItem.category_id == category_id)
            .where((UserPublishedItem.user_id == user_id) | (UserPublishedItem.user_id == None))
            .order_by(VintedItem.price)
        )
        result = await session.execute(stmt)
        unpublished_items = result.scalars().all()
        return unpublished_items
