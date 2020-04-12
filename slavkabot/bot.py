import logging
import telethon as tele
from telethon.events import NewMessage

from slavkabot import handlers


logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config):
        logger.info('Initiating bot')
        self.name = 'sluvka_bot'

        api_id = config['API_ID']
        api_hash = config['API_HASH']

        if config['USE_PROXY']:
            conn = tele.connection.ConnectionTcpMTProxyRandomizedIntermediate
            proxy_address = (config['PROXY_HOST'],
                             config['PROXY_PORT'],
                             config['PROXY_SECRET'])
            logger.info(f'Using proxy {proxy_address[0]}:{proxy_address[1]}')

            self.bot = tele.TelegramClient('bot', api_id, api_hash,
                                           connection=conn,
                                           proxy=proxy_address)
        else:
            self.bot = tele.TelegramClient('bot', api_id, api_hash)

        self.register_handlers()
        self.bot.start(bot_token=config['TOKEN'])
        logger.info('Bot initiated')

        # self.handler = Handler(self.bot)

    def register_handlers(self):
        logger.info('Registering handlers')
        self.bot.add_event_handler(handlers.greet,
                                   NewMessage(pattern='/greet'))
        self.bot.add_event_handler(handlers.respond,
                                   NewMessage(pattern=f'.*(@{self.name}).*'))

    def start(self):
        logger.info('Starting bot')
        self.bot.run_until_disconnected()
