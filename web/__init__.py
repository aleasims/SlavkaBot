from flask import Flask, request

from slavkabot.slavka import Slavka

greeting = Slavka().greeting()

web = Flask(__name__)


@web.route('/')
def home():
    return f'<h1>{greeting}</h1>'


@web.route('/<token>', methods=['POST'])
def telegram_ping(token):
    web.logger().info(f'Request from {request.remote_addr}')
    return ''
