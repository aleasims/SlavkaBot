import os
import asyncio
import logging
from telethon import events

from slavkabot.slavka import Slavka
from slavkabot.members import get_member

best_chat = os.getenv('best_chat')
slavka = Slavka()
logger = logging.getLogger(__name__)


async def greet(event):
    await event.respond(slavka.greeting())
    raise events.StopPropagation


async def respond(event):
    message = event.message.text
    # remove botname from message text
    message = message.replace(event.pattern_match.group(1), '').strip()
    author = get_member(event.message.from_id)
    await event.respond(slavka.respond(message, author))
    raise events.StopPropagation


class Handler:
    def __init__(self, client):
        self.client = client
        for handler in self.get_handlers():
            client.add_event_handler(handler)

    # @events.register(events.NewMessage(pattern='(?i).*(слав|slav|/speak|@sluvka_bot).*'))
    # async def _echo(self, event):
    #     await event.respond(slavka.random_phrase())
    #     raise events.StopPropagation

    @events.register(events.NewMessage(pattern='^!'))
    async def _announce(self, event):
        await self.client.send_message(best_chat, event.text[1:])
        raise events.StopPropagation

    @events.register(events.NewMessage(outgoing=True, pattern='ping'))
    async def _ping(self, event):
        """Say "pong" whenever you send "ping", then delete both messages."""
        resp = await event.respond('pong')
        await asyncio.sleep(5)
        await self.client.delete_messages(event.chat_id, [event.id, resp.id])
        raise events.StopPropagation

    @events.register(events.ChatAction)
    async def handler(self, event):
        """Welcome every new user."""
        if event.user_joined:
            await event.reply(slavka.welcome())

    def get_handlers(self, mode='all'):
        if mode == 'all':
            return [getattr(self, field)
                    for field in dir(self)
                    if field[0] == '_' and field[1] != '_']
        else:
            return []
