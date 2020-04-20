import logging

from telethon import TelegramClient, events
from telethon.events import NewMessage

from slavkabot import Slavka

logger = logging.getLogger(__name__)


class HandlerManager:
    def __init__(self, client: TelegramClient, slavka: Slavka):
        self.client = client
        self.slavka = slavka

        self.client.add_event_handler(self.greet)
        self.client.add_event_handler(self.init_dialog)

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage())
    async def init_dialog(self, event: NewMessage.Event):
        if event.message.mentioned:
            logger.info(f'Init dialog for chat ID: {event.chat_id}')
            self.client.add_event_handler(
                self.respond, NewMessage(chats=event.chat_id))
            self.client.add_event_handler(
                self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))

    async def respond(self, event: NewMessage.Event):
        logger.info(f'Active dialog with chat ID: {event.chat_id}')
        event.respond(self.slavka.random_phrase())

    async def stfu(self, event: NewMessage.Event):
        logger.info(f'Stop dialog for chat ID: {event.chat_id}')
        self.client.remove_event_handler(
            self.respond, NewMessage(chats=event.chat_id))
        self.client.remove_event_handler(
            self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))
