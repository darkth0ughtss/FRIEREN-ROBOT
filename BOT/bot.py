from pyrogram import Client as PyrogramClient
from .config import bot_token, api_id, api_hash




# Initialize the Pyrogram bot client
bot = PyrogramClient(
    "my_bot_pyrogram",  # Name of the session
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
)

BOT_ID = 7205145628
