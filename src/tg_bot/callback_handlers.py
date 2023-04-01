from aiogram import types
from aiogram.types import CallbackQuery

from .bot import dp, bot
from .keyboards import *
from .utils import send_new_items_to_user, edit_message_with_keyboard
from .states import NewCategory
from src.tg_bot.db_handler import get_user_categories, get_categories, add_category_to_user, get_unpublished_items_by_category


# callback handlers

@dp.callback_query_handler(lambda call: call.data == "show_new_items")
async def show_new_items_handler(call: CallbackQuery):
    user_id = call.from_user.id

    await send_new_items_to_user(user_id)

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "my_categories")
async def my_categories_handler(call: CallbackQuery):
    user_id = call.from_user.id

    user_categories = await get_user_categories(user_id)

    keyboard = categories_keyboard(user_categories)
    await edit_message_with_keyboard(call.message, text="Your categories:", keyboard=keyboard)

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "back_to_menu")
async def back_to_menu_handler(call: CallbackQuery):
    user_id = call.from_user.id

    keyboard = menu_keyboard()

    await edit_message_with_keyboard(call.message, text="Menu:", keyboard=keyboard)

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "add_new_category")
async def add_new_category_handler(call: CallbackQuery):
    user_id = call.from_user.id

    all_categories = await get_categories()

    keyboard = all_categories_keyboard(all_categories)
    await bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="All categories:",
                                reply_markup=keyboard)

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "add_new_one")
async def add_new_one_handler(call: CallbackQuery):
    user_id = call.from_user.id

    await bot.send_message(chat_id=user_id, text="Please enter the name of the new category you want to add:")

    await NewCategory.InputCategoryName.set()

    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith("add_category_"))
async def add_category_handler(call: CallbackQuery):
    user_id = call.from_user.id
    category_id = int(call.data.split("_")[-1])

    await add_category_to_user(user_id, category_id)

    await bot.send_message(chat_id=user_id, text="Category added successfully.")

    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith("category_") and call.data.endswith("_view_items"))
async def category_view_items_handler(call: CallbackQuery):
    user_id = call.from_user.id
    category_id = int(call.data.split("_")[1])

    # Retrieve unpublished items for the user and the selected category
    unpublished_items = await get_unpublished_items_by_category(user_id, category_id)

    # Send the items to the user
    if unpublished_items:
        for item in unpublished_items:
            await send_new_item(user_id, item)
    else:
        await bot.send_message(chat_id=user_id, text="No new items in this category.")

    # Return to the "My categories" keyboard
    user_categories = await get_user_categories(user_id)
    keyboard = categories_keyboard(user_categories)
    await bot.send_message(chat_id=user_id, text="Your categories:", reply_markup=keyboard)

    await call.answer()


