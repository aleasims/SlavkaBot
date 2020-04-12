from flask import Flask

from slavkabot.slavka import Slavka

greeting = Slavka().greeting()

web = Flask(__name__)


@web.route('/')
def home():
    return f'<h1>{greeting}</h1>'


if __name__ == "__main__":
    web.run()
