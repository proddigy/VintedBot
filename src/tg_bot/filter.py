from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from .db_handler import get_admin_users_ids


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: Message) -> bool:
        admin_ids = await get_admin_users_ids()
        checker = message.from_user.id in admin_ids
        return checker == self.is_admin
