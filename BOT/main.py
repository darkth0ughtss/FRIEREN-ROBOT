# BOT/main.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .bot import bot
from .handlers import *  # Import all handlers
from .game.tictactoe.tictactoe_handler import *
from .utils.whispher import *
from .morehandlers import *
from .dev_cmd import *
from .quizbot import *
from .group import *


if __name__ == "__main__":

    bot.run()
