# handlers/start_handler.py

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ..imgs_config import get_random_start_image
from ..bot import bot
from pymongo import MongoClient
from ..config import MONGO_URL
import time
import sys
import pyrogram


mongo_client = MongoClient(MONGO_URL)
db = mongo_client["THE-BOT"]
users_collection = db["USERS"]

# Define versions
VERSION = "1.0.1"  # Update this as per your bot's version
PYTHON_VERSION = sys.version.split(" ")[0]
PYROGRAM_VERSION = pyrogram.__version__

# Uptime calculation
start_time = time.time()

@bot.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_first_name = message.from_user.first_name
    user_id = message.from_user.id

    # Save user ID to the USERS collection
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "first_name": user_first_name})

    # Delete the /start command message sent by the user
    await message.delete()

    # List of possible captions
    captions = [
        (
            f"๏ 𝙾𝚔𝚊𝚎𝚛𝚒, 𝙸'𝚖 [{client.me.first_name}](tg://user?id={client.me.id})\n♥ 𝙸𝚝'𝚜 𝚜𝚘 𝚐𝚘𝚘𝚍 𝚝𝚘 𝚜𝚎𝚎 𝚢𝚘𝚞.\n\n"
            "➻ 𝙻𝚎𝚝'𝚜 𝚎𝚖𝚋𝚊𝚛𝚔 𝚘𝚗 𝚊 𝚗𝚎𝚠 𝚊𝚍𝚟𝚎𝚗𝚝𝚞𝚛𝚎 𝚝𝚘𝚐𝚎𝚝𝚑𝚎𝚛. "
            "𝙸'𝚖 𝚑𝚎𝚛𝚎 𝚝𝚘 𝚊𝚜𝚜𝚒𝚜𝚝 𝚢𝚘𝚞 𝚠𝚒𝚝𝚑 𝚊𝚗𝚢𝚝𝚑𝚒𝚗𝚐 𝚢𝚘𝚞 𝚗𝚎𝚎𝚍.\n\n\n"
            "☘️ 𝙲𝚑𝚎𝚌𝚔 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚋𝚎𝚕𝚘𝚠 ☘️"
        ),
        (
            f"๏ 𝙷𝚎𝚢 𝚂𝚎𝚗𝚙𝚊𝚒, 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 [{client.me.first_name}](tg://user?id={client.me.id})\n♥ 𝙳𝚎𝚕𝚒𝚐𝚑𝚝𝚎𝚍 𝚝𝚘 𝚜𝚎𝚎 𝚢𝚘𝚞.\n\n"
            "➻ 𝙻𝚎𝚝'𝚜 𝚋𝚎𝚐𝚒𝚗 𝚊 𝚗𝚎𝚠 𝚓𝚘𝚞𝚛𝚗𝚎𝚢 𝚝𝚘𝚐𝚎𝚝𝚑𝚎𝚛. "
            "𝙸'𝚖 𝚑𝚎𝚛𝚎 𝚝𝚘 𝚑𝚎𝚕𝚙 𝚢𝚘𝚞 𝚠𝚒𝚝𝚑 𝚊𝚗𝚢 𝚚𝚞𝚎𝚜𝚝𝚒𝚘𝚗𝚜 𝚢𝚘𝚞 𝚖𝚊𝚢 𝚑𝚊𝚟𝚎.\n\n\n"
            "☘️ 𝙲𝚑𝚎𝚌𝚔 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚋𝚎𝚕𝚘𝚠 ☘️"
        ),
        (
            f"๏ 𝙷𝚒 𝚂𝚎𝚗𝚙𝚊𝚒, 𝙸'𝚖 [{client.me.first_name}](tg://user?id={client.me.id})\n♥ 𝙳𝚒𝚍 𝚢𝚘𝚞 𝚖𝚒𝚜𝚜 𝚖𝚎? 𝙸'𝚟𝚎 𝚖𝚒𝚜𝚜𝚎𝚍 𝚢𝚘𝚞!\n\n"
            "➻ 𝙻𝚎𝚝'𝚜 𝚜𝚝𝚊𝚛𝚝 𝚘𝚞𝚛 𝚓𝚘𝚞𝚛𝚗𝚎𝚢 𝚊𝚐𝚊𝚒𝚗. "
            "𝙸'𝚖 𝚊𝚕𝚠𝚊𝚢𝚜 𝚑𝚎𝚛𝚎 𝚝𝚘 𝚊𝚜𝚜𝚒𝚜𝚝 𝚢𝚘𝚞 𝚠𝚒𝚝𝚑 𝚠𝚑𝚊𝚝𝚎𝚟𝚎𝚛 𝚢𝚘𝚞 𝚗𝚎𝚎𝚍.\n\n\n"
            "☘️ 𝙲𝚑𝚎𝚌𝚔 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚋𝚎𝚕𝚘𝚠 ☘️"
        )
    ]

    # Step 1: Send "𝚂𝚝𝚊𝚛𝚝𝚒𝚗𝚐....."
    start_msg = await message.reply_text("𝚂𝚝𝚊𝚛𝚝𝚒𝚗𝚐.....")
    await asyncio.sleep(0.35)

    # Step 2: Edit message to "𝚆𝚎𝚕𝚌𝚘𝚖𝚎 {user's first name} 𝚋𝚊𝚋𝚢 𝚑𝚘𝚠 𝚊𝚛𝚎 𝚞𝚑𝚑..."
    await start_msg.edit_text(f"𝚆𝚎𝚕𝚌𝚘𝚖𝚎 {user_first_name} 𝚋𝚊𝚋𝚢 𝚑𝚘𝚠 𝚊𝚛𝚎 𝚞𝚑𝚑...")
    await asyncio.sleep(0.35)

    # Step 3: Delete the message and send "💕"
    await start_msg.delete()
    emoji_msg = await message.reply_text("💕")
    await asyncio.sleep(0.35)

    # Step 4: Edit the emoji to "⚡️"
    await emoji_msg.edit_text("⚡️")
    await asyncio.sleep(0.35)

    # Step 5: Edit the emoji to "✨"
    await emoji_msg.edit_text("✨")
    await asyncio.sleep(0.35)

    # Step 6: Delete the emoji message and send random start image
    await emoji_msg.delete()
    start_image = get_random_start_image()
    caption = random.choice(captions)  # Select a random caption

    buttons = [
        [InlineKeyboardButton("💫 𝘈𝘋𝘋 𝘔𝘌 𝘛𝘖 𝘠𝘖𝘜𝘙 𝘎𝘙𝘖𝘜𝘗 💫", url="https://telegram.dog/frierenzbot?startgroup=true")],
        [
            InlineKeyboardButton("✨𝘊𝘖𝘔𝘔𝘈𝘕𝘋𝘚 ✨", callback_data="commands"),
            InlineKeyboardButton("🌿𝘚𝘶𝘱𝘱𝘰𝘳𝘵 🌿", url="https://t.me/DominosXd")
        ],
        [ 
            InlineKeyboardButton("🔔𝘜𝘱𝘥𝘢𝘵𝘦𝘴🔔", url="https://t.me/DominosNetwork"),
            InlineKeyboardButton("ℹ️ 𝘉𝘖𝘛-𝘐𝘕𝘍𝘖", callback_data="bot_info")
        ]
    ]
    await client.send_photo(
        chat_id=message.chat.id,
        photo=start_image,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
 
@bot.on_callback_query(filters.regex("bot_info"))
async def bot_info_callback(client, q):
    # Generate a random ping value between 3 and 18 with two decimal places
    ping_ms = f"{random.uniform(3, 18):.2f}"

    # Calculate uptime
    up = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    
    txt = (
        f"🏓 Ping : {ping_ms} ms\n"
        f"📈 Uptime : {up}\n"
        f"🤖 Bot's version: {VERSION}\n"
        f"🐍 Python's version: {PYTHON_VERSION}\n"
        f"🔥 Pyrogram's version : {PYROGRAM_VERSION}"
    )
    await q.answer(txt, show_alert=True)
    return