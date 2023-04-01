from aiogram.dispatcher.filters.state import StatesGroup, State


class NewCategory(StatesGroup):
    InputCategoryName = State()
