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

        if telegram.get('use_proxy'):
            conn = tele.connection.ConnectionTcpMTProxyRandomizedIntermediate
            proxy = (telegram['proxy']['host'],
                     telegram['proxy']['port'],
                     telegram['proxy']['secret'])
            logger.info(f'Using proxy {proxy[0]}:{proxy[1]}')

            self.client = tele.TelegramClient('bot',
                                              telegram['api_id'],
                                              telegram['api_hash'],
                                              connection=conn,
                                              proxy=proxy)
        else:
            self.client = tele.TelegramClient('bot',
                                              telegram['api_id'],
                                              telegram['api_hash'])

        self.client.start(bot_token=telegram['token'])
        logger.info('Started Telegram Client')

        self.client.me = self.client.loop.run_until_complete(self.client.get_me())

        bot = config.get('bot', {})

        self.slavka = Slavka(bot.get('model', {}), bot.get('phrases_path'))
        logger.info('Initiated Slavka')

        self.handler = HandlerManager(self.client, self.slavka,
                                      max_dialogs=bot.get('max_dialogs'),
                                      cache_size=bot.get('cache_size'))

        logger.info(f'Bot initiated')

    def start(self):
        logger.info(f'Starting bot')
        self.client.run_until_disconnected()
