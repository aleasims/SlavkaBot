from flask import Flask

from slavkabot.slavka import Slavka

greeting = Slavka().greeting()

app = Flask(__name__)


@app.route('/')
def home():
    return f'<h1>{greeting}</h1>'


@app.route('/<token>', methods=['POST'])
def telegram_ping(token):
    return ''
