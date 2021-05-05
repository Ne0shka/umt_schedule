import sys

from loguru import logger
from vkbottle.bot import Bot

from src.blueprints import bps
from src.config import BOT_TOKEN
from src.middlewares.no_bot_middleware import NoBotMiddleware

logger.remove()
logger.add(sys.stdout, level="INFO")


def init_bot():
    bot = Bot(token=BOT_TOKEN)
    setup_blueprints(bot)
    setup_middlewares(bot)
    return bot


def setup_blueprints(bot: Bot):
    for bp in bps:
        bp.load(bot)


def setup_middlewares(bot: Bot):
    bot.labeler.message_view.register_middleware(NoBotMiddleware)


bot = init_bot()
