"""
SQLAlchemy models for the database
"""

from sqlalchemy import Column, Integer, BigInteger, String, Numeric, Text, ForeignKey, Boolean, LargeBinary, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Parser related models
class VintedItem(Base):
    __tablename__ = 'vinted_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    unique_id = Column(BigInteger, unique=True, nullable=False)
    price = Column(Numeric(10, 3), nullable=False)
    brand_name = Column(String(255), nullable=False)
    size = Column(String(10), nullable=False)
    url = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=False)

    category_id = Column(Integer, ForeignKey('saved_categories.id'))
    category = relationship("Category")
    users_published = relationship("UserPublishedItem", back_populates="item")

    def as_dict(self):
        return {
            "title": self.title,
            "unique_id": self.unique_id,
            "price": self.price,
            "brand_name": self.brand_name,
            "size": self.size,
            "url": self.url,
            "image_path": self.image_path,
            "category_id": self.category_id,
        }


class Category(Base):
    __tablename__ = 'saved_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    relationship("TelegramBotUser", secondary="user_categories")


# Telegram related models
class TelegramBotUser(Base):
    __tablename__ = 'telegram_bot_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    notifications = Column(Boolean, default=False, nullable=False)

    relationship("Category", secondary="user_categories")
    published_items = relationship("UserPublishedItem", back_populates="user")

    def __repr__(self):
        return f"TelegramBotUser(id={self.id}, username='{self.username}', first_name='{self.first_name}', active={self.active}, notifications={self.notifications})"


class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('telegram_bot_users.id', ondelete='CASCADE'))
    is_admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"AdminUser(id={self.id}, user_id={self.user_id}, is_admin={self.is_admin})"


class UserCategory(Base):
    __tablename__ = 'user_categories'

    user_id = Column(Integer, ForeignKey("telegram_bot_users.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("saved_categories.id", ondelete="CASCADE"), primary_key=True)


class UserPublishedItem(Base):
    __tablename__ = 'user_published_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('telegram_bot_users.id'))
    item_id = Column(Integer, ForeignKey('vinted_items.id'))

    user = relationship("TelegramBotUser", back_populates="published_items")
    item = relationship("VintedItem", back_populates="users_published")
