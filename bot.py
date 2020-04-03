import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler

LOG_MSG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_MSG)
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()

elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(
            HEROKU_APP_NAME, TOKEN))

else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    bot.send_message(update.message.chat_id, "привет, пёс, это Славка!")


SLAVKA_PHRASES = [
    'версута сын собаки!',
    'ору с гей-мерзкого чата)',
    'фу блять мерзкий войсчат',
    'какая нахуй телега, мир сошел с ума...',
    'у меня эта помойка работает еле-еле потому что в России блять запрещена',
    'ПО ФОРМУЛЕ!!!',
    'предлагаю присесть в коридоре',
    'МАРАТ ДА ПО ФОРМУЛЕ!',
    'Гребной коронавирус...',
    'ты как рубашку снял, Петров?',
    'Марти одевает подштанники...',
    'почему Степан генерирует рандомный вопрос, начинающийся со слова "почему", скорее всего не имеющий разумного ответа, к тому же с изначально сомнительным утверждением в теле вопроса?',
    'ЗДЕСЬ ЛЮДЕЙ ЕБУТ',
    'челы, вы...',
    'АААААААААААААААААААААААААААА',
    'может тебе неудобства доставить',
    'Сань ты что по этому поводу скажешь?',
    'ровно 2,573 человека',
    'ля, почему вы форсите столько хуйни с двача? 90 процентов контента, который вы оттуда скидываете, несмешно и кринжово',
    'общего чата не заслуживает',
    'то чувство, когда у Узумаки Наруто больше посещений философии, чем у меня...',
    'комната умирает',
    'чел, ты...',
    'ляг поспи...',
    'дип фэйк закрыли',
    'rest in RIP Степан...',
    'никово...',
    'Челы, вы... Где нахуй?',
    'Почему не в палате?',
    'Хули в комнате пусто :(',
    "oh u're approaching me?",
    'ещё сука молчит в ВК не отвечает на крысу...',
    'вовремя я заболел... впрочем, будь я на месте, наверн ничего бы не изменилось?',
    'красава Марти',
    'найс режим',
    'я болею(',
    'Чел а если серьезно?',
    'Его идеи... полная хуйня',
    'чел... ты ебанулся?',
    'уберемся на скорую руку',
    'ладно, я подъеду, челы...',
    'УРА)'
]


def speak_handler(bot, update):
    id_ = update.effective_user["id"]
    number = random.randint(0, len(SLAVKA_PHRASES))
    phrase = SLAVKA_PHRASES[number]
    logger.info("User {} asked for speak: {}".format(id_, phrase))
    bot.send_message(update.message.chat_id, phrase)
    # update.message.reply_text(phrase)


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("speak", speak_handler))

    run(updater)
