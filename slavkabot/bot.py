import os, sys
import telethon as tele
from telethon import events
import logging
from datetime import timedelta

from slavka import Slavka
from handlers import handlers

# from handlers import logger, handlers
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
            proxy_port = os.getenv('proxy_port')
            proxy_secret = os.getenv('proxy_secret')

            self.bot = tele.TelegramClient('bot', api_id, api_hash, connection=tele.connection.ConnectionTcpMTProxyRandomizedIntermediate,
                proxy=(proxy_hostname, int(proxy_port), proxy_secret)).start(bot_token=bot_token)
        
        elif mode == 'heroku':
            self.bot = tele.TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
        
        else:
            logger.error('No mode specified!')
            sys.exit(1)
        
        for handler in handlers:
            self.bot.add_event_handler(handler)
                
    def start(self):
        self.bot.run_until_disconnected()

if __name__ == '__main__':
    bot = Bot()
    bot.start()