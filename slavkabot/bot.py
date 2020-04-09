import os
import sys
import logging

import telethon as tele

from slavkabot.handlers import Handler

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()


class Bot:
    def __init__(self):
        mode = os.getenv('mode')
        bot_token = os.getenv('token')
        api_id = os.getenv('api_id')
        api_hash = os.getenv('api_hash')
        mode = os.getenv('mode')

        if mode == 'dev':
            proxy_hostname = os.getenv('proxy_hostname')
            proxy_port = int(os.getenv('proxy_port'))
            proxy_secret = os.getenv('proxy_secret')

            conn = tele.connection.ConnectionTcpMTProxyRandomizedIntermediate

            self.bot = tele.TelegramClient('bot', api_id, api_hash,
                                           connection=conn,
                                           proxy=(proxy_hostname,
                                                  proxy_port,
                                                  proxy_secret))

        elif mode == 'heroku':
            self.bot = tele.TelegramClient('bot', api_id, api_hash)
            logger.info('A'*100)
            logger.info(print(self.bot.session)
            logger.info(print(self.bot.session.port)
            logger.info(print(self.bot.session.server_address)
        else:
            logger.error('No mode specified!')
            sys.exit(1)

        self.bot.start(bot_token=bot_token)
        self.Handler=Handler(self.bot)

    def start(self):
        self.bot.run_until_disconnected()
