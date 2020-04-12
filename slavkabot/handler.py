import logging
import os

from telethon import events
from telethon.events import NewMessage
from telethon.errors.rpcerrorlist import BotMethodInvalidError

from slavkabot.slavka import Slavka

best_chat = os.getenv('best_chat')
slavka = Slavka()
logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, bot):
        self.bot = bot
        for event, handler in self.handlers():
            self.bot.client.add_event_handler(handler, event)

    def handlers(self):
        yield from {
            NewMessage(pattern='/greet'): self.greet,
            NewMessage(pattern=f'.*(@{self.bot.name}).*'): self.respond
        }.items()

    async def greet(self, event):
        await event.respond(slavka.greeting())
        raise events.StopPropagation

    async def respond(self, event):
        try:
            context = await self.bot.client.get_messages(
                self.bot.chat_id, limit=slavka.context_size)
        except BotMethodInvalidError as err:
            # Chat history is not available to bots with privacy mode.
            logger.warn(f'Cannot obtain chat history: {err}. Using only received message.')
            context = [event.message]

        await event.respond(slavka.respond(context, self.bot.name))
        raise events.StopPropagation

    # @events.register(events.NewMessage(pattern='(?i).*(слав|slav|/speak|@sluvka_bot).*'))
    # async def _echo(self, event):
    #     await event.respond(slavka.random_phrase())
    #     raise events.StopPropagation

    # @events.register(events.NewMessage(pattern='^!'))
    # async def _announce(self, event):
    #     await self.client.send_message(best_chat, event.text[1:])
    #     raise events.StopPropagation

    # @events.register(events.NewMessage(outgoing=True, pattern='ping'))
    # async def _ping(self, event):
    #     """Say "pong" whenever you send "ping", then delete both messages."""
    #     resp = await event.respond('pong')
    #     await asyncio.sleep(5)
    #     await self.client.delete_messages(event.chat_id, [event.id, resp.id])
    #     raise events.StopPropagation

    # @events.register(events.ChatAction)
    # async def handler(self, event):
    #     """Welcome every new user."""
    #     if event.user_joined:
    #         await event.reply(slavka.welcome())

    # def get_handlers(self, mode='all'):
    #     if mode == 'all':
    #         return [getattr(self, field)
    #                 for field in dir(self)
    #                 if field[0] == '_' and field[1] != '_']
    #     else:
    #         return []
