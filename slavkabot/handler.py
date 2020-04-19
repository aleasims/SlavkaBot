import logging
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

        self.slavka = Slavka(context_size=self.cache_size)
        self.cache = deque(maxlen=self.cache_size)

        for handler in self.handlers():
            self.bot.client.add_event_handler(handler)

    def handlers(self):
        return [
            self.greet,
            self.cache,
            self.respond,
        ]

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage())
    async def cache(self, event):
        self.cache.append(event.message)
        logger.debug(f'Cached entity {self.message}')

    @events.register(NewMessage(pattern=f'.*(@{BOT_NAME}).*'))
    async def respond(self, event):
        self.bot.chage_state(BotState.DIALOG)
        await event.respond(self.slavka.respond(self.cache,
                                                self.BOT_NAME))
        raise events.StopPropagation
