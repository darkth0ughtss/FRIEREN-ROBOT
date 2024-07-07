import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from BOT.bot import bot
from BOT.imgs_config import PAT_IMAGES  # Assuming you have a list of pat images

# Command handler for /pat
@bot.on_message(filters.command("pat") & filters.group)
async def pat_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗼𝗿 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝘁𝗼 𝗽𝗮𝘁 𝘁𝗵𝗲𝗺.")
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            await message.reply_text(f"Could not find user {username}.")
            return

    # Check if the bot is being patted
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        await message.reply_text("You can't pat a bot, but thanks for the gesture! 🤖")
        return

    if user_a.id == user_b.id:
        await message.reply_text("You can't pat yourself. You deserve pats from others!")
        return

    # Get a random pat image URL
    pat_image_url = random.choice(PAT_IMAGES)

    # Send the pat message with the image
    await client.send_photo(
        chat_id=message.chat.id,
        photo=pat_image_url,
        caption=f"🤗 **[{user_a.first_name}](tg://user?id={user_a.id})** gave a warm pat to **[{user_b.first_name}](tg://user?id={user_b.id})**! So sweet! 💖",
        parse_mode=ParseMode.MARKDOWN
    )
