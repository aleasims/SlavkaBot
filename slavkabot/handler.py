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
        self.client.add_event_handler(self.init_dialog)

    @events.register(NewMessage(pattern='/greet'))
    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    @events.register(NewMessage())
    async def init_dialog(self, event: NewMessage.Event):
        if event.message.mentioned:
            logger.info(f'Init dialog for chat ID: {event.chat_id}')
            respond_event = NewMessage(chats=event.chat_id)
            stop_event = NewMessage(chats=event.chat_id, pattern='/stfu')
            logger.info(f'Respond event: {respond_event}')
            logger.info(f'Stop event: {stop_event}')
