import logging

import telethon as tele

from slavkabot import HandlerManager
from slavkabot import Slavka

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config):
        logger.info('Initiating bot')
        self.mode = config['mode']
        self.name = config.get('bot_name', '')

        telegram = config['telegram']

        if telegram.get('USE_PROXY'):
            conn = tele.connection.ConnectionTcpMTProxyRandomizedIntermediate
            proxy_address = (telegram['PROXY_HOST'],
                             telegram['PROXY_PORT'],
                             telegram['PROXY_SECRET'])
            logger.info(f'Using proxy {proxy_address[0]}:{proxy_address[1]}')

            self.client = tele.TelegramClient('bot',
                                              telegram['API_ID'],
                                              telegram['API_HASH'],
                                              connection=conn,
                                              proxy=proxy_address)
        else:
            self.client = tele.TelegramClient('bot',
                                              telegram['API_ID'],
                                              telegram['API_HASH'])

        self.client.start(bot_token=telegram['TOKEN'])
        logger.info('Started Telegram Client')

        bot = config.get('bot', {})

        self.slavka = Slavka(bot.get('phrases_path'),
                             model_cfg=bot.get('model', {}))
        logger.info('Initiated Slavka')

        self.handler = HandlerManager(self.client, self.slavka,
                                      max_dialogs=bot.get('MAX_DIALOGS'),
                                      cache_size=bot.get('CACHE_SIZE'))

        logger.info(f'Bot initiated')

    def start(self):
        logger.info(f'Starting bot')
        self.client.run_until_disconnected()
