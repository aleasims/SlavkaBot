from slavkabot.config import build_config
from slavkabot.bot import Bot


if __name__ == '__main__':
    config = build_config('config.yml')
    bot = Bot(config)
    bot.start()
