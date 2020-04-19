import logging
import time
from collections import deque

from telethon import events
from telethon.events import NewMessage

from slavkabot.slavka import Slavka
from slavkabot.state import BotState

logger = logging.getLogger(__name__)


class Handler:
    BOT_NAME = ''

    def __init__(self, bot, cache_size=10):
        self.bot = bot
        Handler.BOT_NAME = self.bot.name
        self.cache_size = cache_size

        self.cached = {}
        self.slavka = Slavka(context_size=self.cache_size)

    def handlers(self):
        return [
            self.greet,
            self.stop_dialog,
            self.checkout_state,
            self.cache,
            self.init_dialog,
            self.respond,
        ]

    @staticmethod
    def now():
        return time.time()

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage(pattern='/stfu'))
    async def stop_dialog(self, event):
        if self.bot.state == BotState.DIALOG:
            self.bot.change_state(BotState.IDLE)
        raise events.StopPropagation

    @events.register(NewMessage())
    async def cache(self, event):
        if event.chat_id not in self.cached:
            self.cached[event.chat_id] = deque(maxlen=self.cache_size)
        self.cached[event.chat_id].append(event.message)
        logger.debug(f'Cached entity {event.message}')

    @events.register(NewMessage())
    async def checkout_state(self, event):
        passed = self.now() - self.bot.last_checkout
        if passed > self.bot.dialog_timeout and \
                self.bot.state == BotState.DIALOG:
            self.bot.change_state(BotState.IDLE)

    @events.register(NewMessage(pattern=f'.*(@{BOT_NAME}).*'))
    async def init_dialog(self, event):
        self.bot.change_state(BotState.DIALOG)

    @events.register(NewMessage())
    async def respond(self, event):
        self.bot.last_checkout = self.now()
        if self.bot.state == BotState.DIALOG:
            await event.respond(self.slavka.respond(
                list(self.cached[event.chat_id]), self.BOT_NAME))
        raise events.StopPropagation
