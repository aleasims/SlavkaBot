from slavkabot.config import build_config
from slavkabot.bot import Bot
import logging
import os


def main():
    config = build_config()
    logger = logging.getLogger(__name__)
    logger.info(f'CWD={os.getcwd()}')
    bot = Bot(config)
    bot.start()
