import logging
import telethon as tele

from slavkabot.handlers import Handler


logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, config):
        logger.info('Initiating bot')

        api_id = config['API_ID']
        api_hash = config['API_HASH']
        token = config['TOKEN']

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

        self.bot.start(bot_token=token)
        logger.info('Bot initiated')

        self.Handler = Handler(self.bot)

    def start(self):
        logger.info('Starting bot')
        self.bot.run_until_disconnected()
