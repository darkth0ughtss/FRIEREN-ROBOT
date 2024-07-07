from ..bot import bot 


from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from ..config import MONGO_URL, OWNER_ID  # Ensure config is correct and OWNER_ID is a list of IDs


# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["THE-BOT"]
users_collection = db["USERS"]
groups_collection = db["GROUPS"]

@bot.on_message(filters.command("botinfo") & filters.user(OWNER_ID))
async def botinfo_handler(client: Client, message: Message):
    try:
        total_users = users_collection.count_documents({})
        total_groups = groups_collection.count_documents({})
        await message.reply_text(f"TOTAL NUMBER OF USERS: {total_users}\nTOTAL NUMBER OF GROUPS: {total_groups}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@bot.on_message(filters.new_chat_members)
async def new_group_handler(client: Client, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title

    # Save group chat ID and title to the GROUPS collection
    if not groups_collection.find_one({"chat_id": chat_id}):
        groups_collection.insert_one({"chat_id": chat_id, "title": chat_title})

async def send_dice_response(client: Client, message: Message, emoji: str):
    try:
        await client.send_dice(
            chat_id=message.chat.id,
            emoji=emoji,
            reply_to_message_id=message.id
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@bot.on_message(filters.command("ludo"))
async def ludo_handler(client: Client, message: Message):
    await send_dice_response(client, message, "🎲")

@bot.on_message(filters.command("dart"))
async def dart_handler(client: Client, message: Message):
    await send_dice_response(client, message, "🎯")

@bot.on_message(filters.command("bowl"))
async def bowl_handler(client: Client, message: Message):
    await send_dice_response(client, message, "🎳")

@bot.on_message(filters.command("football"))
async def football_handler(client: Client, message: Message):
    await send_dice_response(client, message, "⚽")

@bot.on_message(filters.command("basket"))
async def basket_handler(client: Client, message: Message):
    await send_dice_response(client, message, "🏀")

@bot.on_message(filters.command("slot"))
async def slot_handler(client: Client, message: Message):
    await send_dice_response(client, message, "🎰")
