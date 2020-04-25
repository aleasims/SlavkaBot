import logging
import requests
from collections import deque
from typing import Dict
import asyncio
import random

from telethon import TelegramClient, events
from telethon.events import NewMessage
from telethon.tl import types
from telethon.tl.custom import Button, MessageMediaPhoto

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

        self.empty_ch = '⠀'
        self.alive_ch = '⭕️'
        self.dead_ch = '❌'
        self.react_butt_id = 'r_'
        self.game_butt_id = 'g_'
        self.gift_butt_id = 'gft'
        reactions = ['👍', '😏', '🤔', '😧', '😑']
        self.reactions_markup = self.client.build_reply_markup(
            [[Button.inline(emoji, self.react_butt_id + emoji) for emoji in reactions]], inline_only=True)

        self.client.add_event_handler(self.greet, NewMessage(pattern='/greet'))
        self.client.add_event_handler(self.gift, NewMessage(pattern='/gift'))
        self.client.add_event_handler(self.play, NewMessage(
            pattern=r'/play\s?(\d*)'))
        self.client.add_event_handler(self.on_click, events.CallbackQuery())
        self.client.add_event_handler(self.on_click_reactions, events.CallbackQuery(
            pattern=self.react_butt_id + r'(\S+)\s?(\d*)'))
        self.client.add_event_handler(self.on_click_gift, events.CallbackQuery(
            pattern=self.gift_butt_id))
        self.client.add_event_handler(self.on_click_game, events.CallbackQuery(
            pattern=self.game_butt_id + r'(\d+)\s(\d+)\s(\d+)'))
        self.client.add_event_handler(self.on_click_game_finish, events.CallbackQuery(
            pattern=self.game_butt_id + 'f'))
        self.client.add_event_handler(self.add_buttons, NewMessage())
        self.client.add_event_handler(self.init_dialog, NewMessage())

    async def greet(self, event: NewMessage.Event):
        await event.respond(self.slavka.greeting())
        raise events.StopPropagation

    async def gift(self, event: NewMessage.Event):
        msg = event.message
        msg.text = 'Here is a gift for you!'
        msg.reply_markup = self.client.build_reply_markup(
            [Button.inline('🎁', data=self.gift_butt_id)],
            inline_only=True)
        await msg.respond(msg)

    async def on_click(self, event: events.CallbackQuery.Event):
        logger.info(f'Clicked button with data={event.data}')

    async def on_click_gift(self, event: events.CallbackQuery.Event):
        link = requests.get('https://meme-api.herokuapp.com/gimme').json()['url']
        logger.info(f'Gift link: {link}')
        image = requests.get(link).content
        logger.info(f'Image size: {len(image)} bytes')
        await event.answer(f'You have unpacked a gift!')
        await event.edit(buttons=None, file=image)

    async def on_click_reactions(self, event: events.CallbackQuery.Event):
        text, num = event.pattern_match.group(1).decode(
            'utf-8'), event.pattern_match.group(2)
        num = (int(num) if num else 0) + 1
        mes = await event.get_message()
        logger.info(
            f'{get_member(event.sender_id)} clicked reaction button {text} {num} (mes_id={mes.id}, chat_id={event.chat_id})')

        buttons = (await mes.get_buttons())[0]  # first row
        new_text = text + ' ' + str(num)
        new_buttons = [butt if (butt.data != event.data) else Button.inline(new_text, self.react_butt_id + new_text)
                       for butt in buttons]

        await event.answer(f'You {text} this')
        await event.edit(buttons=new_buttons)

    async def on_click_game(self, event: events.CallbackQuery.Event):
        mes = await event.get_message()
        logger.info(
            f'{get_member(event.sender_id)} clicked game button (mes_id={mes.id}, chat_id={event.chat_id})')

        lvl, cur, sel = [int(x) for x in event.pattern_match.groups()]
        buttons = (await mes.get_buttons())[0]  # first row
        complexity = 4 * len(buttons)**3
        chance = lvl / (lvl + complexity)

        if sel != cur and random.random() < chance:
            buttons[cur] = Button.inline(self.empty_ch)
            buttons[sel] = Button.inline(self.dead_ch)
            await mes.edit('🎉 Победа! 🎉', buttons=buttons)
            await asyncio.sleep(1)
            await mes.edit(buttons=Button.inline("Получить награду", self.game_butt_id + 'f'))
        else:
            new_cur = random.randrange(len(buttons) - 1)
            if new_cur >= cur:
                new_cur = new_cur + 1
            lvl += 1
            game_state = self.game_butt_id + str(lvl) + ' ' + str(new_cur)
            buttons = [Button.inline(self.empty_ch if i != new_cur else self.alive_ch,
                                     game_state + ' ' + str(i)) for i in range(len(buttons))]
            await mes.edit(buttons=buttons)

        raise events.StopPropagation

    async def on_click_game_finish(self, event: events.CallbackQuery.Event):
        mes = await event.get_message()
        await mes.edit('Axaxa наебал', buttons=None)

    async def add_buttons(self, event: NewMessage.Event):
        types_react_to = (types.MessageMediaDocument,
                          types.MessageMediaPhoto, types.MessageMediaWebPage)
        if isinstance(event.media, types_react_to) and not event.sticker:
            msg = event.message
            logger.info('MESSAGE DIR:')
            logger.info('\n'.join(['****' + repr(getattr(msg, k)) for k in dir(msg) if not k.startswith('__')]))

            msg.reply_markup = self.reactions_markup
            sender = await msg.get_sender()
            msg.text = f'__From @{sender.username}__ \n' + msg.text

            await msg.delete()
            await msg.respond(msg)

            logger.info(
                f'Added buttons (mes_id={event.message.id}, chat_id={event.chat_id})')

    async def play(self, event: NewMessage.Event):
        logger.info(
            f'Started game (chat_id={event.chat_id})')
        default_num_buttons = 5

        num_buttons = event.pattern_match.group(1)
        num_buttons = default_num_buttons if not num_buttons else int(num_buttons)
        lvl = 0
        cur = random.randrange(num_buttons)
        game_state = self.game_butt_id + str(lvl) + ' ' + str(cur)
        buttons = [Button.inline(self.empty_ch if i != cur else self.alive_ch,
                                 game_state + ' ' + str(i)) for i in range(num_buttons)]
        play_markup = self.client.build_reply_markup(buttons)

        await event.respond(self.empty_ch, buttons=play_markup)

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
