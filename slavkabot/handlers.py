import logging
from telethon import events

from slavka import Slavka

class Handler:
    def __init__(self, client):
        self.client = client
        for handler in self.get_handlers():
            client.add_event_handler(handler)
        
    @events.register(events.NewMessage(pattern='/greet'))
    async def _greet(self, event):
        await event.respond(slavka.greeting())
        raise events.StopPropagation

    @events.register(events.NewMessage(pattern='(?i)(слав|slav|/speak)'))
    async def _echo(self, event):
        await event.respond(slavka.random_phrase())
        raise events.StopPropagation

    def get_handlers(self, mode='all'):
        if mode=='all':
            return [getattr(self, field) for field in dir(self) if field[0]=='_' and field[1]!='_']

    # @events.register(events.NewMessage(pattern='^!'))
    # async def _announce(self, event):
    #     await event.respond(event.text[])
    #     raise events.StopPropagation

slavka = Slavka()

if __name__ == "__main__":
    pass