import time
from multiprocessing import Process

from flask import Flask

from slavkabot.bot import Bot
from slavkabot.slavka import Slavka

slavka = Slavka()
web = Flask(__name__)


@web.route('/')
def home():
    return f'<h1>{slavka.greeting}</h1>'


if __name__ == "__main__":
    bot = Bot()
    time.sleep(15)
    Process(target=bot.start).start()
    web.run()
