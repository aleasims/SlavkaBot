from slavkabot.config import build_config, download_model
from slavkabot.bot import Bot


def main():
    config = build_config()
    download_model()
    bot = Bot(config)
    bot.start()
