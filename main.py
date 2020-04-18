from slavkabot.config import build_config
from slavkabot.bot import Bot
import logging
import os


def main():
    config = build_config()
    logger = logging.getLogger(__name__)
    path = os.getcwd()
    logger.info(f'CWD={path}')
    bot = Bot(config)
    bot.start()


if __name__ == '__main__':
    main()
