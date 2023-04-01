from tg_bot.bot import dp, on_startup, on_shutdown
from tg_bot.command_handlers import *
from tg_bot.callback_handlers import *

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)