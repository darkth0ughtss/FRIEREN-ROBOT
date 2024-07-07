from pyrogram import filters, enums
from pyrogram.types import Message
from ..bot import bot

# Helper function to extract user
async def extract_user(c, m):
    if m.reply_to_message:
        return m.reply_to_message.from_user.id, None, None
    elif len(m.command) > 1:
        if m.command[1].startswith("@"):
            try:
                user = await c.get_users(m.command[1])
                return user.id, user.first_name, user.username
            except Exception as e:
                return None, None, None
        else:
            return int(m.command[1]), None, None
    else:
        return m.from_user.id, None, None

# Helper function to mention user in HTML
async def mention_html(name, user_id):
    return f'<a href="tg://user?id={user_id}">{name}</a>'

@bot.on_message(
    filters.command("id") & (filters.group | filters.private),
)
async def id_info(c: bot, m: Message): # type: ignore
    ChatType = enums.ChatType
    user_id, user_first_name, username = await extract_user(c, m)
    try:
        if user_id and len(m.text.split()) == 2:
            txt = f"Given user's id: <code>{user_id}</code>"
            await m.reply_text(txt, parse_mode=enums.ParseMode.HTML)
            return
        elif m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP] and not m.reply_to_message:
            await m.reply_text(text=f"This Group's ID is <code>{m.chat.id}</code>\nYour ID <code>{m.from_user.id}</code>")
            return
        elif m.chat.type == ChatType.PRIVATE and not m.reply_to_message:
            await m.reply_text(text=f"Your ID is <code>{m.chat.id}</code>.")
            return
    except Exception as e:
        await m.reply_text(str(e))
        return
    if user_id:
        if m.reply_to_message and m.reply_to_message.forward_from:
            user1 = m.reply_to_message.from_user
            user2 = m.reply_to_message.forward_from
            orig_sender = await mention_html(user2.first_name, user2.id)
            orig_id = f"<code>{user2.id}</code>"
            fwd_sender = await mention_html(user1.first_name, user1.id)
            fwd_id = f"<code>{user1.id}</code>"
            await m.reply_text(
                text=f"""Original Sender - {orig_sender} (<code>{orig_id}</code>)
Forwarder - {fwd_sender} (<code>{fwd_id}</code>)""",
                parse_mode=enums.ParseMode.HTML,
            )
        else:
            try:
                user = await c.get_users(user_id)
            except Exception:
                await m.reply_text(
                    text="""Failed to get user
      Peer ID invalid, I haven't seen this user anywhere earlier, maybe username would help to know them!"""
                )
                return
            await m.reply_text(
                f"{(await mention_html(user.first_name, user.id))}'s ID is <code>{user.id}</code>.",
                parse_mode=enums.ParseMode.HTML,
            )
    elif m.chat.type == ChatType.PRIVATE:
        text = f"Your ID is <code>{m.chat.id}</code>."
        if m.reply_to_message:
            if m.forward_from:
                text += f"Forwarded from user ID <code>{m.forward_from.id}</code>."
            elif m.forward_from_chat:
                text += f"Forwarded from user ID <code>{m.forward_from_chat.id}</code>."
        await m.reply_text(text)
    else:
        text = f"Chat ID <code>{m.chat.id}</code>\nYour ID <code>{m.from_user.id}</code>"
        await m.reply_text(text)
    return
