import logging

from telethon import TelegramClient, events
from telethon.events import NewMessage

from slavkabot import Slavka

logger = logging.getLogger(__name__)


class HandlerManager:
    def __init__(self, name: str, client: TelegramClient, slavka: Slavka):
        self.bot_name = name
        self.client = client
        self.slavka = slavka

        self.client.add_event_handler(self.greet)

        init_event = NewMessage(pattern=f'.*(@{self.bot_name}).*')
        self.client.add_event_handler(self.init_dialog, init_event)

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event):
        logger.info(f'Type of event: {type(event)}')
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    async def init_dialog(self, event):
        logger.info(f'Dir event: {event}')
        logger.info(f'Chat ID: {event.chat_id}')
