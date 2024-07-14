import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .bot import bot
from .handlers import *  # Import all handlers
from .game.tictactoe.tictactoe_handler import *
from .utils.whispher import *
from .morehandlers import *
from .dev_cmd import *
from .quizbot import *
from .group import *
from .helper import *

# Configure logging (optional, if not configured elsewhere)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    bot.run()
