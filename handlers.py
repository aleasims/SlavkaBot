import logging

from slavka import Slavka

slavka = Slavka()


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()


def start_handler(update, context):
    id_ = update.effective_user['id']
    logger.info(f'User {id_} started bot')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=slavka.greeting())


def speak_handler(update, context):
    id_ = update.effective_user['id']
    phrase = slavka.random_phrase()
    logger.info(f'User {id_} asked for speak: {phrase}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=phrase)
