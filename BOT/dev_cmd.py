import os
import logging
import subprocess
from pyrogram import filters
from .bot import bot
from .config import OWNER_IDS  # Replace with the actual list of bot owner's Telegram IDs

# Configure logging
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w')
logger = logging.getLogger(__name__)

def owner_filter(_, __, message):
    return message.from_user.id in OWNER_IDS

@bot.on_message(filters.command("restart") & filters.create(owner_filter))
def restart_bot(client, message):
    message.reply_text("Restarting bot...")
    os.execlp("python3", "python3", "-m", "BOT")

@bot.on_message(filters.command("logs") & filters.create(owner_filter))
def send_logs(client, message):
    log_file = "bot.log"
    if os.path.exists(log_file):
        with open(log_file, "rb") as f:
            client.send_document(message.chat.id, f, caption="Here are the logs.")
    else:
        message.reply_text("No log file found.")