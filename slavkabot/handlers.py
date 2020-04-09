import logging
from telethon import events

from slavka import Slavka

class Handlers:
    @staticmethod
    @events.register(events.NewMessage(pattern='/greet'))
    async def _greet(event):
        await event.respond(slavka.greeting())
        raise events.StopPropagation

    @staticmethod
    @events.register(events.NewMessage(pattern='/speak'))
    async def _echo(event):
        await event.respond(slavka.random_phrase())

slavka = Slavka()
handlers = [getattr(Handlers, field) for field in dir(Handlers) if field[0]=='_' and field[1]!='_']

if __name__ == "__main__":
    print (handlers)