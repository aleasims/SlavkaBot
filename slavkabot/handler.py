import logging
from collections import deque

from telethon import TelegramClient, events
from telethon.events import NewMessage

from slavkabot import Slavka
from slavkabot import get_member

logger = logging.getLogger(__name__)


class HandlerManager:
    def __init__(self, client: TelegramClient, slavka: Slavka):
        self.client = client
        self.slavka = slavka

        self.cache = {}
        self.cache_size = 25

        self.client.add_event_handler(self.greet)
        self.client.add_event_handler(self.init_dialog)

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage())
    async def init_dialog(self, event: NewMessage.Event):
        if event.message.mentioned:
            if event.chat_id not in self.cache:
                logger.info(f'Init dialog for chat ID: {event.chat_id}')
                self.cache[event.chat_id] = deque(maxlen=self.cache_size)
                self.client.add_event_handler(
                    self.respond, NewMessage(chats=event.chat_id))
                self.client.add_event_handler(
                    self.stfu, NewMessage(chats=event.chat_id,
                                          pattern='/stfu'))

    async def respond(self, event: NewMessage.Event):
        logger.info(f'Active dialog with chat ID: {event.chat_id}')

        message = (get_member(event.message.from_id), event.message.text)
        self.cache[event.chat_id].append(message)
        logging.debug(f'Cached message: {message}')

        await event.respond(self.slavka.respond(self.cache[event.chat_id]))
        raise events.StopPropagation

    async def stfu(self, event: NewMessage.Event):
        logger.info(f'Stop dialog for chat ID: {event.chat_id}')
        self.client.remove_event_handler(
            self.respond, NewMessage(chats=event.chat_id))
        self.client.remove_event_handler(
            self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))
        raise events.StopPropagation
