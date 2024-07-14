from traceback import format_exc
from typing import Tuple

from pyrogram.enums import MessageEntityType as EntityType
from pyrogram.types import Message

from ..bot import bot as app
from ..db.user_db import get_user_info


async def extract_user(c: app, m: Message) -> Tuple[int, str, str]:
    user_id = None
    user_first_name = None
    user_name = None

    # Check if the message is a reply to another message
    if m.reply_to_message and m.reply_to_message.from_user:
        user_id = m.reply_to_message.from_user.id
        user_first_name = m.reply_to_message.from_user.first_name
        user_name = m.reply_to_message.from_user.username

    elif len(m.text.split()) > 1:
        # Check if there are entities in the message
        if len(m.entities) > 1:
            required_entity = m.entities[1]
            if required_entity.type == EntityType.TEXT_MENTION:
                user_id = required_entity.user.id
                user_first_name = required_entity.user.first_name
                user_name = required_entity.user.username
            elif required_entity.type in (EntityType.MENTION, EntityType.PHONE_NUMBER):
                user_found = m.text[
                    required_entity.offset : (required_entity.offset + required_entity.length)
                ]

                try:
                    user_found = int(user_found)
                except ValueError:
                    user_found = str(user_found)

                try:
                    user = await get_user_info(user_found)
                    user_id = user["user_id"]
                    user_first_name = user["user_first_name"]
                    user_name = user["username"]
                except KeyError:
                    try:
                        user = await c.get_users(user_found)
                    except Exception:
                        try:
                            user_r = await c.resolve_peer(user_found)
                            user = await c.get_users(user_r.user_id)
                        except Exception as ef:
                            return await m.reply_text(f"User not found! Error: {ef}")
                    user_id = user.id
                    user_first_name = user.first_name
                    user_name = user.username
                except Exception as ef:
                    return await m.reply_text(f"Error retrieving user: {ef}")
        
        else:
            user_input = m.text.split()[1]
            try:
                user_id = int(user_input)
            except ValueError:
                user_id = user_input if user_input.startswith("@") else None

            if user_id is not None:
                try:
                    user = await get_user_info(user_id)
                    user_first_name = user["user_first_name"]
                    user_name = user["username"]
                except Exception:
                    try:
                        user = await c.get_users(user_id)
                    except Exception:
                        try:
                            user_r = await c.resolve_peer(user_id)
                            user = await c.get_users(user_r.user_id)
                        except Exception as ef:
                            return await m.reply_text(f"User not found! Error: {ef}")
                    user_first_name = user.first_name
                    user_name = user.username

    else:
        user_id = m.from_user.id
        user_first_name = m.from_user.first_name
        user_name = m.from_user.username

    return user_id, user_first_name, user_name
