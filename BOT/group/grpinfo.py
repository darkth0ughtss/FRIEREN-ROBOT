from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import MONGO_URL, OWNER_ID  # Ensure config is correct and OWNER_ID is a list of IDs
from pymongo import MongoClient
from ..bot import bot 
from pyrogram.types import Message, ChatPrivileges



# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["THE-BOT"]
users_collection = db["USERS"]
groups_collection = db["GROUPS"]

@bot.on_message(filters.command("gcinfo"))
async def groupinfo_handler(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        members_count = await client.get_chat_members_count(chat_id)
        group_info = groups_collection.find_one({"chat_id": chat_id})

        if group_info:
            group_title = group_info.get("title", "Unknown")
            response = (f"Group Title: {group_title}\n"
                        f"Chat ID: {chat_id}\n"
                        f"Members Count: {members_count}")
        else:
            response = (f"Chat ID: {chat_id}\n"
                        f"Members Count: {members_count}\n"
                        "Group info not found in the database.")

        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Include this function in your main bot initialization if needed
async def get_chat_members_count(client: Client, chat_id: int):
    try:
        count = await client.get_chat_members_count(chat_id)
        return count
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
