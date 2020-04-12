from .config import build_config
from .bot import Bot


if __name__ == "__main__":
    config = build_config()
    bot = Bot(config)
    bot.start()
