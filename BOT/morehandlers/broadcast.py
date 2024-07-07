from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from ..config import MONGO_URL, OWNER_ID  # Ensure config is correct and OWNER_ID is a list of IDs
from ..bot import bot
# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["THE-BOT"]
users_collection = db["USERS"]
groups_collection = db["GROUPS"]

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def handle_broadcast(client: Client, message: Message):
    # Check if the message is a reply to another message
    if message.reply_to_message:
        # Check if the replied message contains text or photo with or without caption
        if message.reply_to_message.text:
            # Extract the broadcast message from the replied message
            broadcast_text = message.reply_to_message.text
            # Retrieve all user IDs from the database
            user_ids = [doc['user_id'] for doc in users_collection.find({}, {'_id': 0, 'user_id': 1})]
            # Retrieve all group IDs from the database
            group_ids = [doc['chat_id'] for doc in groups_collection.find({}, {'_id': 0, 'chat_id': 1})]

            # Send the broadcast message to users
            for user_id in user_ids:
                try:
                    await client.send_message(user_id, broadcast_text)
                except Exception as e:
                    print(f"Error sending message to user {user_id}: {e}")

            # Send the broadcast message to groups
            for group_id in group_ids:
                try:
                    await client.send_message(group_id, broadcast_text)
                except Exception as e:
                    print(f"Error sending message to group {group_id}: {e}")

            # Calculate the total count of users and groups
            total_count = len(user_ids) + len(group_ids)

            # Send confirmation message to the sudo user with total count
            confirmation_message = f"Broadcast sent successfully!\n\nMessages sent to {total_count} users and groups."
            await message.reply_text(confirmation_message)
        
        elif message.reply_to_message.photo:
            # Extract the photo file ID and caption from the replied message
            photo_file_id = message.reply_to_message.photo.file_id
            caption = message.reply_to_message.caption
            
            # Retrieve all user IDs from the database
            user_ids = [doc['user_id'] for doc in users_collection.find({}, {'_id': 0, 'user_id': 1})]
            # Retrieve all group IDs from the database
            group_ids = [doc['chat_id'] for doc in groups_collection.find({}, {'_id': 0, 'chat_id': 1})]

            # Send the photo with caption to users
            for user_id in user_ids:
                try:
                    await client.send_photo(user_id, photo_file_id, caption=caption)
                except Exception as e:
                    print(f"Error sending photo to user {user_id}: {e}")

            # Send the photo with caption to groups
            for group_id in group_ids:
                try:
                    await client.send_photo(group_id, photo_file_id, caption=caption)
                except Exception as e:
                    print(f"Error sending photo to group {group_id}: {e}")

            # Calculate the total count of users and groups
            total_count = len(user_ids) + len(group_ids)

            # Send confirmation message to the sudo user with total count
            confirmation_message = f"Broadcast sent successfully!\n\nPhotos sent to {total_count} users and groups."
            await message.reply_text(confirmation_message)

    else:
        await message.reply_text("🛑 Please reply to a message containing the text or photo you want to broadcast.")
