import threading
from tg_bot.bot import dp, on_startup, on_shutdown
from tg_bot.command_handlers import *
from tg_bot.callback_handlers import *
from parser_scheduler import main as parser_main


def start_parser_thread():
    parser_thread = threading.Thread(target=parser_main, daemon=True)
    parser_thread.start()


if __name__ == "__main__":
    start_parser_thread()

    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
