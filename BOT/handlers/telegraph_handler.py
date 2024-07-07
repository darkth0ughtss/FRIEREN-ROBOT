import os
import asyncio
import aiofiles
from pyrogram import filters
from ..bot import bot
from ..features.telegrapph import telegraph_client


@bot.on_message(filters.reply & filters.command("up"))
async def upload_image(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("❌ Please reply to an image with /up to upload it to Telegraph.")
        return

    # Download the image to the local device
    file_id = message.reply_to_message.photo.file_id
    file_path = await client.download_media(file_id)

    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()

    # Upload the image to Telegraph in a separate thread
    loop = asyncio.get_running_loop()
    try:
        telegraph_url = await loop.run_in_executor(None, telegraph_client.upload_image, content)
    finally:
        # Delete the local image file
        await aiofiles.os.remove(file_path)

    # Reply with the Telegraph URL
    await message.reply(f"✅ Image uploaded to Telegraph: {telegraph_url}")


@bot.on_message(filters.reply & filters.command("upvid"))
async def upload_video(client, message):
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply("❌ Please reply to a video with /upvid to upload it to Telegraph.")
        return

    # Download the video to the local device
    file_id = message.reply_to_message.video.file_id
    file_path = await client.download_media(file_id)

    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()

    # Upload the video to Telegraph in a separate thread
    loop = asyncio.get_running_loop()
    try:
        telegraph_url = await loop.run_in_executor(None, telegraph_client.upload_file, content)  # Assuming the same function for videos
    finally:
        # Delete the local video file
        await aiofiles.os.remove(file_path)

    # Reply with the Telegraph URL
    await message.reply(f"✅ Video uploaded to Telegraph: {telegraph_url}")
