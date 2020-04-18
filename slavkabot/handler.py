import logging

from telethon import events
from telethon.events import NewMessage
from telethon.errors.rpcerrorlist import BotMethodInvalidError

from slavkabot.slavka import Slavka

logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, bot):
        self.bot = bot
        self.slavka = Slavka()
        for event, handler in self.handlers():
            self.bot.client.add_event_handler(handler, event)

    def handlers(self):
        yield from {
            NewMessage(pattern='/greet'): self.greet,
            NewMessage(pattern=f'.*(@{self.bot.name}).*'): self.respond
        }.items()

    async def greet(self, event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    async def respond(self, event):
        try:
            context = await self.bot.client.get_messages(
                self.bot.chat_id, limit=self.slavka.context_size)
        except BotMethodInvalidError as err:
            # Chat history is not available to bots with privacy mode.
            logger.warn(f'Cannot obtain chat history: {err}. Using only received message.')
            context = [event.message]

        await event.respond(self.slavka.respond(context, self.bot.name))
        raise events.StopPropagation
