"""
SQLAlchemy models for the database
"""

from sqlalchemy import Column, Integer, BigInteger, String, Numeric, Text, ForeignKey, Boolean, LargeBinary, \
    UniqueConstraint
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
    size = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    image_url = Column(Text, nullable=False)

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
            "image_url": self.image_url,
            "category_id": self.category_id,
        }

    def __repr__(self):
        return f"VintedItem(id={self.id}, title='{self.title}', unique_id={self.unique_id}, price={self.price}, brand_name='{self.brand_name}', size='{self.size}')"


class Category(Base):
    __tablename__ = 'saved_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=True, default=None)

    relationship("TelegramBotUser", secondary="user_categories")
    relationship("Brand", uselist=False)
    relationship("VintedItem", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', brand_id={self.brand_id})"


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    vinted_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Brand(id={self.id}, name='{self.name}',  vinted_id={self.vinted_id})"


# Telegram related models
class TelegramBotUser(Base):
    """
    Represents a Telegram user
    """
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
    user_id = Column(BigInteger, ForeignKey('telegram_bot_users.id', ondelete='CASCADE'))
    is_admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"AdminUser(id={self.id}, user_id={self.user_id}, is_admin={self.is_admin})"


class UserCategory(Base):
    """
    Many-to-many relationship between users and categories
    """
    __tablename__ = 'user_categories'

    user_id = Column(Integer, ForeignKey("telegram_bot_users.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("saved_categories.id", ondelete="CASCADE"), primary_key=True)


class UserPublishedItem(Base):
    """
    Many-to-many relationship between users and items
    """
    __tablename__ = 'user_published_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('telegram_bot_users.id'))
    item_id = Column(BigInteger, ForeignKey('vinted_items.unique_id'))

    user = relationship("TelegramBotUser", back_populates="published_items")
    item = relationship("VintedItem", back_populates="users_published")

    __table_args__ = (UniqueConstraint('user_id', 'item_id', name='user_item_unique'),)

    __repr__ = __str__ = lambda self: f"UserPublishedItem(id={self.id}, user_id={self.user_id}, item_id={self.item_id})"




