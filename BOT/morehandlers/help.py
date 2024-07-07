# handlers/help_handler.py

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery , InputMediaPhoto
from ..imgs_config import help_command_urls
import random
from ..bot import bot as Client

FEATURES = [
    "𝗔𝗡𝗜𝗠𝗘",
    "𝗖𝗢𝗦𝗣𝗟𝗔𝗬",
    "𝗖𝗢𝗨𝗣𝗟𝗘",
    "𝗖𝗥𝗜𝗖𝗞𝗘𝗧",
    "𝗙𝗢𝗡𝗧",
    "𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠",
    "𝗣𝗜𝗡𝗧𝗘𝗥𝗘𝗦𝗧",
    "𝗦𝗘𝗔𝗥𝗖𝗛",
    "𝗦𝗣𝗢𝗧𝗜𝗙𝗬",
    "𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗣𝗛",
    "𝗧𝗥𝗔𝗡𝗦𝗟𝗔𝗧𝗘",
    "𝗧𝗧𝗦",
    "𝗗𝗜𝗖𝗧𝗜𝗢𝗡𝗔𝗥𝗬",
    "𝗪𝗔𝗜𝗙𝗨",
    "𝗬𝗧",        
    "𝗦𝗢𝗡𝗚",        
    "𝗚𝗔𝗠𝗘𝗦",  
    "𝗙𝗨𝗡",  
    "𝗨𝗧𝗜𝗟𝗦",   
    "𝗪𝗜𝗦𝗣𝗛𝗘𝗥", 
    "𝗟𝗬𝗥𝗜𝗖𝗦",  
    "𝗪𝗘𝗕𝗦𝗦",    
    "𝗠𝗔𝗧𝗛",  
    "𝗣𝗢𝗞𝗘𝗗𝗘𝗫"

]

FEATURE_DETAILS = {
    "𝗔𝗡𝗜𝗠𝗘": "Retrieve anime details with /anime 'title'. Includes title, type, genres, rating, status, dates, episodes, duration, and synopsis.",
    "𝗖𝗢𝗦𝗣𝗟𝗔𝗬": "Get a random cosplay photo with /cosplay.",
    "𝗖𝗢𝗨𝗣𝗟𝗘": "Pair random members as couples for the day with /couple, /couples, or /shipping.",
    "𝗖𝗥𝗜𝗖𝗞𝗘𝗧": "Fetch upcoming cricket match details with /cricket. Includes title, date, teams, venue, and next match button.",
    "𝗙𝗢𝗡𝗧": "Apply font styles to text with /font 'text'. Use inline buttons for styles.",
    "𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠": "Download Instagram reels with /insta 'link'.",
    "𝗣𝗜𝗡𝗧𝗘𝗥𝗘𝗦𝗧": "Download Pinterest media with /pnt 'link'.",
    "𝗦𝗘𝗔𝗥𝗖𝗛": "Search news, web, and images with /bingsearch and /img. Use /news for keyword-based news.",
    "𝗦𝗣𝗢𝗧𝗜𝗙𝗬": "Access Spotify features with commands like /top_playlist, /sp_daily, /sp_trending, etc.",
    "𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗣𝗛": "Upload replied images to Telegraph with /up or /upvid for videos.",
    "𝗧𝗥𝗔𝗡𝗦𝗟𝗔𝗧𝗘": "Translate text with /tr 'target_lang'. Detects and translates from replied text.",
    "𝗧𝗧𝗦": "Convert text to speech (TTS) in English with /tts 'text'.",
    "𝗗𝗜𝗖𝗧𝗜𝗢𝗡𝗔𝗥𝗬": "Search Urban Dictionary with /ud 'term' for definitions.",
    "𝗪𝗔𝗜𝗙𝗨": "Fetch random SFW waifu images with /waifu.",
    "𝗬𝗧": "Download YouTube videos with /yt 'link'.",
    "𝗦𝗢𝗡𝗚": "Search and download songs from YouTube with /song 'name'.",
    "𝗚𝗔𝗠𝗘𝗦": "Start games, bet on coin toss, view leaderboard with commands like /tto, /bet, /topboard, etc. You can also manage virtual stocks with /buystock to buy stocks, /sellstock to sell stocks, /viewmarket to view the market, /viewportfolio to check your portfolio, /petshop to visit the pet shop, /pets to view your pet's information, /profile to view your profile, and /setpfp to set your profile picture. Use /dice for betting on dice roll, /wallet to check your balance, and /bank to manage your bank with commands like deposit, withdraw, and balance.",    "𝗙𝗨𝗡": "Interact with fun commands like /slap, /hug, /kiss, etc.",
    "𝗨𝗧𝗜𝗟𝗦": "You can use commands like /kiss /hug /sex /kickk /slap in group chats.",
    "𝗪𝗜𝗦𝗣𝗛𝗘𝗥": "Send private 'whispers' using /whisper '@username message'. Start with '@botusername' in any chat to activate inline queries.",
    "𝗟𝗬𝗥𝗜𝗖𝗦": "Fetch song lyrics with /lyrics 'song_name'.",
    "𝗪𝗘𝗕𝗦𝗦": "Take screenshots of websites with /ss 'website_link'.",
    "𝗠𝗔𝗧𝗛": "Perform math operations with commands like /add, /substract, /multiply, etc.",
    "𝗣𝗢𝗞𝗘𝗗𝗘𝗫": "Get details about a Pokemon with /pokedex 'pokemon_name'."
}


BUTTONS_PER_PAGE = 9
BUTTONS_PER_ROW = 3

def get_feature_buttons(page=0):
    start = page * BUTTONS_PER_PAGE
    end = start + BUTTONS_PER_PAGE
    features = FEATURES[start:end]

    buttons = []
    for i in range(0, len(features), BUTTONS_PER_ROW):
        buttons.append([InlineKeyboardButton(features[j], callback_data=f"feature_{start + j}") for j in range(i, min(i + BUTTONS_PER_ROW, len(features)))])

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("𝑷𝑹𝑬𝑽𝑰𝑶𝑼𝑺", callback_data=f"paginate_{page - 1}"))
    if end < len(FEATURES):
        pagination_buttons.append(InlineKeyboardButton("𝑵𝑬𝑿𝑻", callback_data=f"paginate_{page + 1}"))

    if pagination_buttons:
        buttons.append(pagination_buttons)

    return buttons


@Client.on_message(filters.command("help"))
async def help_command(client, message):

    # Delete the /start command message sent by the user
    await message.delete()

    buttons = get_feature_buttons()
    caption = "𝘏𝘌𝘙𝘌 𝘐𝘚 𝘛𝘏𝘌 𝘓𝘐𝘚𝘛 𝘖𝘍 𝘈𝘓𝘓 𝘍𝘌𝘈𝘛𝘜𝘙𝘌𝘚"

    # Select a random image URL
    image_url = random.choice(help_command_urls)

    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^feature_"))
async def feature_callback(client, callback_query: CallbackQuery):
    feature_index = int(callback_query.data.split("_")[1])
    feature = FEATURES[feature_index]
    details = FEATURE_DETAILS.get(feature, "No details available for this feature.")
    await callback_query.message.edit_caption(
        caption=details,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="help_back")]])
    )

@Client.on_callback_query(filters.regex(r"^paginate_"))
async def paginate_callback(client, callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    buttons = get_feature_buttons(page)
    await callback_query.message.edit_caption(
        caption="𝘏𝘌𝘙𝘌 𝘐𝘚 𝘛𝘏𝘌 𝘓𝘐𝘚𝘛 𝘖𝘍 𝘈𝘓𝘓 𝘍𝘌𝘈𝘛𝘜𝘙𝘌𝘚",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^help_back"))
async def help_back_callback(client, callback_query: CallbackQuery):
    buttons = get_feature_buttons()
    await callback_query.message.edit_caption(
        caption="𝘏𝘌𝘙𝘌 𝘐𝘚 𝘛𝘏𝘌 𝘓𝘐𝘚𝘛 𝘖𝘍 𝘈𝘓𝘓 𝘍𝘌𝘈𝘛𝘜𝘙𝘌𝘚",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex(r"^commands"))
async def commands_callback(client, callback_query: CallbackQuery):
    buttons = get_feature_buttons()
    caption = "𝘏𝘌𝘙𝘌 𝘐𝘚 𝘛𝘏𝘌 𝘓𝘐𝘚𝘛 𝘖𝘍 𝘈𝘓𝘓 𝘍𝘌𝘈𝘛𝘜𝘙𝘌𝘚"

    # Select a random image URL
    image_url = random.choice(help_command_urls)

    await callback_query.message.edit_media(
        media=InputMediaPhoto(media=image_url, caption=caption),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
