from slavkabot.config import build_config
from slavkabot.bot import Bot


def main():
    config = build_config()
    bot = Bot(config)
    bot.start()
