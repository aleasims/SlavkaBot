import logging
from collections import deque
from typing import Dict

from telethon import TelegramClient, events
from telethon.events import NewMessage
from telethon.tl import types
from telethon.tl.custom import Button

from slavkabot import Slavka
from slavkabot import get_member

logger = logging.getLogger(__name__)


class HandlerManager:
    def __init__(self, client: TelegramClient, slavka: Slavka,
                 max_dialogs: int = 10,
                 cache_size: int = 10):
        self.client = client
        self.slavka = slavka

        self.active_dialogs = set()
        self.max_dialogs = max_dialogs

        self.cache: Dict[int, deque] = {}
        self.cache_size = cache_size

        self.client.add_event_handler(self.greet, NewMessage(pattern='/greet'))
        self.client.add_event_handler(self.on_click, events.CallbackQuery())
        self.client.add_event_handler(self.add_buttons, NewMessage())
        self.client.add_event_handler(self.init_dialog, NewMessage())

    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    async def on_click(self, event: events.CallbackQuery.Event):
        await event.answer('You {} this'.format(event.data.decode('UTF-8')), 100)

    async def add_buttons(self, event: NewMessage.Event):
        markup = self.client.build_reply_markup([[Button.inline('👍'), Button.inline('😏'),
                                                  Button.inline('🤔'), Button.inline('😧'), Button.inline('😑')]], inline_only=True)
        types_react_to = (types.MessageMediaDocument,
                          types.MessageMediaPhoto, types.MessageMediaWebPage)
        if isinstance(event.media, types_react_to) and not event.sticker:
            await event.respond('🤔', buttons=markup)

    async def init_dialog(self, event: NewMessage.Event):
        if event.message.mentioned and \
                event.chat_id not in self.active_dialogs:
            if len(self.active_dialogs) == self.max_dialogs:
                await event.respond('Мне че разорваться чтоль? подожди, я с другими общаюсь!')
                raise events.StopPropagation

            logger.info(f'Init dialog (chat_id={event.chat_id})')
            self.active_dialogs.add(event.chat_id)
            self.client.add_event_handler(
                self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))
            self.client.add_event_handler(
                self.respond, NewMessage(incoming=True, chats=event.chat_id))

    async def respond(self, event: NewMessage.Event):

        logger.info(
            f'Call (chat_id={event.chat_id}): {repr(event.message.text)}')
        message = (get_member(event.message.from_id), event.message.text)

        if event.chat_id not in self.cache:
            self.cache[event.chat_id] = deque(maxlen=self.cache_size)
        self.cache[event.chat_id].append(message)
        logger.debug(f'Cached message: {repr(message[1])} from {message[0]}')

        response = self.slavka.respond(self.cache[event.chat_id])
        logger.info(f'Response ({event.chat_id}): {repr(response)}')

        await event.respond(response)
        raise events.StopPropagation

    async def stfu(self, event: NewMessage.Event):
        logger.info(f'Stop dialog (chat_id={event.chat_id})')
        self.client.remove_event_handler(
            self.respond, NewMessage(incoming=True, chats=event.chat_id))
        self.client.remove_event_handler(
            self.stfu, NewMessage(chats=event.chat_id, pattern='/stfu'))
        self.active_dialogs.remove(event.chat_id)
        raise events.StopPropagation
