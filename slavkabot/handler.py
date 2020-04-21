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

        self.active_dialogs = set()
        self.max_dialogs = 10
        self.cache = {}
        self.cache_size = 10

        self.client.add_event_handler(self.greet)
        self.client.add_event_handler(self.init_dialog)

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage())
    async def init_dialog(self, event: NewMessage.Event):
        if len(self.active_dialogs) == self.max_dialogs:
            await event.respond('Мне че разорваться чтоль?' +
                                'подожди, я с другими общаюсь!')
            raise events.StopPropagation

        if event.message.mentioned and \
                event.chat_id not in self.active_dialogs:
            logger.info(f'Init dialog for chat ID: {event.chat_id}')

            self.active_dialogs.add(event.chat_id)
            self.client.add_event_handler(
                self.stfu, NewMessage(chats=event.chat_id,
                                      pattern='/stfu'))
            self.client.add_event_handler(
                self.respond, NewMessage(chats=event.chat_id))

    async def respond(self, event: NewMessage.Event):
        logger.info(f'Active respond for {event.chat_id} chat')
        message = (get_member(event.message.from_id), event.message.text)

        if event.chat_id not in self.cache:
            self.cache[event.chat_id] = deque(maxlen=self.cache_size)
        self.cache[event.chat_id].append(message)
        logging.debug(f'Cached message: {message}')

        response = self.slavka.respond(self.cache[event.chat_id])
        logger.info(f'Response ({event.chat_id}): {repr(response)}')

        await event.respond(response)
        raise events.StopPropagation

    async def stfu(self, event: NewMessage.Event):
        logger.info(f'Stop dialog for chat ID: {event.chat_id}')
        self.client.remove_event_handler(
            self.respond, NewMessage(chats=event.chat_id))
        self.client.remove_event_handler(
            self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))
        self.active_dialogs.remove(event.chat_id)
        raise events.StopPropagation
