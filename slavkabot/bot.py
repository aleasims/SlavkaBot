import logging

import telethon as tele

from slavkabot.handler import Handler
from slavkabot.state import BotState

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config):
        logger.info('Initiating bot')
        # TODO: obtain this dynamicly
        self.name = 'sluvka_bot'
        self.chat_id = -1001280237846

        api_id = config['API_ID']
        api_hash = config['API_HASH']

        if config['USE_PROXY']:
            conn = tele.connection.ConnectionTcpMTProxyRandomizedIntermediate
            proxy_address = (config['PROXY_HOST'],
                             config['PROXY_PORT'],
                             config['PROXY_SECRET'])
            logger.info(f'Using proxy {proxy_address[0]}:{proxy_address[1]}')

            self.client = tele.TelegramClient('bot', api_id, api_hash,
                                              connection=conn,
                                              proxy=proxy_address)
        else:
            self.client = tele.TelegramClient('bot', api_id, api_hash)

        self.client.start(bot_token=config['TOKEN'])
        logger.info('Started Telegram Client')

        self.handler = Handler(self)
        for handler in self.handler.handlers():
            self.client.add_event_handler(handler)
        logger.info('Registered handlers')

        self.state = BotState.IDLE
        logger.info(f'Bot initiated')

    def chage_state(self, state):
        self.state = state
        logger.debug(f'Bot state changed to {state}')

    def start(self):
        logger.info(f'Starting bot ({self.state})')
        self.client.run_until_disconnected()
