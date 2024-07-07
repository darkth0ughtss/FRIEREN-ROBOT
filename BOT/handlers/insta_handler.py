import os
from pyrogram import filters
from ..bot import bot
from ..features.insta import download_instagram_reel
import shutil

# Feature: Download Instagram media
@bot.on_message(filters.command("insta"))
async def insta_command(client, message):
    if len(message.command) < 2:
        await message.reply("❌ 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎𝑛 𝐼𝑛𝑠𝑡𝑎𝑔𝑟𝑎𝑚 𝑚𝑒𝑑𝑖𝑎 𝑙𝑖𝑛𝑘. 𝑈𝑠𝑎𝑔𝑒: /𝑖𝑛𝑠𝑡𝑎 '𝑖𝑛𝑠𝑡𝑎𝑔𝑟𝑎𝑚_𝑚𝑒𝑑𝑖𝑎_𝑙𝑖𝑛𝑘'")
        return
    
    media_link = message.command[1]
    user_id = message.from_user.id
    message_id = message.id
    download_path = f"downloads/{user_id}_{message_id}"
    os.makedirs(download_path, exist_ok=True)
    
    downloading_message = await message.reply("⬇️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝘁𝗵𝗲 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗥𝗲𝗲𝗹, 𝗽𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁...")
    
    video_path = download_instagram_reel(media_link, download_path)
    
    try:
        if video_path:
            await client.send_video(video=video_path, chat_id=message.chat.id)
            os.remove(video_path)
        else:
            await message.reply("❌ 𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗺𝗲𝗱𝗶𝗮. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗵𝗲𝗰𝗸 𝘁𝗵𝗲 𝗹𝗶𝗻𝗸 𝗮𝗻𝗱 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.")
    except Exception as e:
        await message.reply("⚠️ 𝐴𝑛 𝑒𝑟𝑟𝑜𝑟 𝑜𝑐𝑐𝑢𝑟𝑟𝑒𝑑")
    
    # Delete the downloading message
    await client.delete_messages(chat_id=message.chat.id, message_ids=[downloading_message.id])
    
    shutil.rmtree(download_path)
