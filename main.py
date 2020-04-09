from threading import Thread

from flask import Flask

from slavkabot.bot import Bot
from slavkabot.slavka import Slavka

slavka = Slavka()
web = Flask(__name__)


@web.route('/')
def home():
    return f'<h1>{slavka.greeting}</h1>'


bot = Bot()
bot_proc = Thread(target=bot.start)
bot_proc.start()
