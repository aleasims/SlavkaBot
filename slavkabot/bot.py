import os
import sys

from telegram.ext import CommandHandler, Updater

import handlers
from handlers import logger

mode = os.getenv('MODE')
TOKEN = os.getenv('TOKEN')

if mode == 'dev':
    def run(updater):
        updater.start_polling()
elif mode == 'heroku':
    def run(updater):
        PORT = int(os.environ.get('PORT', '8443'))
        HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
        updater.start_webhook(listen='0.0.0.0',
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}')
else:
    logger.error('No MODE specified!')
    sys.exit(1)


if __name__ == '__main__':
    logger.info('Starting bot')
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(
        CommandHandler('start', handlers.start_handler))
    updater.dispatcher.add_handler(
        CommandHandler('speak', handlers.speak_handler))
    updater.dispatcher.add_handler(
        handlers.VerboseHandler(handlers.empty_callback))

    run(updater)
