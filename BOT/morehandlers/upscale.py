# Copyright 2023 Qewertyy, MIT License

import os
from pyrogram import filters
from ..bot import bot as app
from ..utils import getFile, UpscaleImages

BOT_USERNAME = "FrierenzBot"

@app.on_message(filters.command("upscale"))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("Replay to an image?")
    msg = await message.reply("Wait A Min.. Upscalling Your Image")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"), caption=f"Upscaled By @{BOT_USERNAME}")
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}")