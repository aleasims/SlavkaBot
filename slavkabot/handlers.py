import logging
import os
from telethon import events

from slavka import Slavka

best_chat = os.getenv('best_chat')

class Handler:
    def __init__(self, client):
        self.client = client
        for handler in self.get_handlers():
            client.add_event_handler(handler)
        
    @events.register(events.NewMessage(pattern='/greet'))
    async def _greet(self, event):
        await event.respond(slavka.greeting())
        raise events.StopPropagation

    # @events.register(events.NewMessage(pattern='(?i).*(слав|slav|/speak|@sluvka_bot).*'))
    # async def _echo(self, event):
    #     await event.respond(slavka.random_phrase())
    #     raise events.StopPropagation

    @events.register(events.NewMessage(pattern='.*@sluvka_bot.*'))
    async def _respond(self, event):
        await event.respond(slavka.random_phrase())
        raise events.StopPropagation

    @events.register(events.NewMessage(pattern='^!'))
    async def _announce(self, event):
        await self.client.send_message(best_chat, event.text[1:])
        raise events.StopPropagation

    @events.register(events.NewMessage(outgoing=True, pattern='ping'))
    async def _ping(self, event):
        # Say "pong" whenever you send "ping", then delete both messages
        m = await event.respond('pong')
        await asyncio.sleep(5)
        await client.delete_messages(event.chat_id, [event.id, m.id])
        raise events.StopPropagation

    @events.register(events.ChatAction)
    async def handler(self, event):
        # Welcome every new user
        if event.user_joined:
            await event.reply(slavka.Welcome())

    def get_handlers(self, mode='all'):
        if mode=='all':
            return [getattr(self, field) for field in dir(self) if field[0]=='_' and field[1]!='_']
        else:
            return []

slavka = Slavka()

if __name__ == "__main__":
    pass