from threading import RLock
from time import perf_counter
from typing import List, Tuple, Union

from cachetools import TTLCache
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus
from pyrogram.types import CallbackQuery, Message

THREAD_LOCK = RLock()

ADMIN_CACHE = TTLCache(maxsize=512, ttl=(60 * 30), timer=perf_counter)
TEMP_ADMIN_CACHE_BLOCK = TTLCache(maxsize=512, ttl=(60 * 10), timer=perf_counter)

async def admin_cache_reload(m: Union[Message, CallbackQuery], status: str = None) -> List[Tuple[int, str, bool, str, bool]]:
    with THREAD_LOCK:
        if isinstance(m, CallbackQuery):
            m = m.message
        if status is not None:
            TEMP_ADMIN_CACHE_BLOCK[m.chat.id] = status

        try:
            if TEMP_ADMIN_CACHE_BLOCK[m.chat.id] in ("autoblock", "manualblock"):
                return []
        except KeyError:
            pass

        admin_list = [
            (
                member.user.id,
                f"@{member.user.username}" if member.user.username else member.user.first_name,
                member.privileges.is_anonymous,
                member.custom_title if member.custom_title else "admin",  # Admin title
                member.status == ChatMemberStatus.OWNER  # Is owner
            )
            async for member in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS)
            if not member.user.is_deleted
        ]

        ADMIN_CACHE[m.chat.id] = admin_list
        TEMP_ADMIN_CACHE_BLOCK[m.chat.id] = "autoblock"

        return admin_list
