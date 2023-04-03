"""
This module contains keyboards for telegram bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.db_client.models import Category


def menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    show_new_items_btn = InlineKeyboardButton("Show new items", callback_data="show_new_items")
    my_categories_btn = InlineKeyboardButton("My categories", callback_data="my_categories")
    settings_btn = InlineKeyboardButton("Settings", callback_data="settings")
    keyboard.add(show_new_items_btn, my_categories_btn, settings_btn)
    return keyboard


def categories_keyboard(categories: list[Category]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        keyboard.add(InlineKeyboardButton(category.name, callback_data=f"category_{category.id}_view_items"))

    add_new_category_btn = InlineKeyboardButton("Add new category", callback_data="add_new_category")
    back_to_menu_btn = InlineKeyboardButton("Back to menu", callback_data="back_to_menu")
    keyboard.add(add_new_category_btn, back_to_menu_btn)
    return keyboard


def all_categories_keyboard(categories: list[Category]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        keyboard.add(InlineKeyboardButton(category.name, callback_data=f"add_category_{category.id}"))

    add_new_one_btn = InlineKeyboardButton("Add new one", callback_data="add_new_one")
    back_to_menu_btn = InlineKeyboardButton("Back to menu", callback_data="back_to_menu")
    keyboard.add(add_new_one_btn, back_to_menu_btn)
    return keyboard
