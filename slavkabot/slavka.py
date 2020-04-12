import random
import logging
from typing import List

from telethon.tl.custom import Message

from slavkabot.members import get_member
from ChatBotAI.Responder import ChatBotAI

logger = logging.getLogger(__name__)


class Slavka:
    def __init__(self, phrases='slavkabot/phrases.txt', context_size=5):
        self.context_size = context_size
        with open(phrases, 'r', encoding='utf-8') as f:
            self.phrases = [phrase.strip() for phrase in f.readlines()]

        self.chat_bot_ai = ChatBotAI()
        self.chat_bot_ai.load_model()

    def greeting(self):
        return "Батя в здании!"

    def welcome(self):
        return "Добро пожаловать в хату!"

    def random_phrase(self):
        return random.choice(self.phrases)

    def respond(self, context: List[Message], botname: str):
        context = self.parse_context(context, botname)
        logger.debug(f'Feeding context: {context}')

        # TODO: change to sensible response
        out_text = self.chat_bot_ai.respond(context)
        # TODO: Filter out_text till Slavka's response
        filter_idx = out_text.find('EOM')
        if filter_idx > 2:
            out_text = out_text[:filter_idx-2]
        return out_text

    def parse_context(self,
                      messages: List[Message],
                      botname: str = '') -> str:
        """
        Example output:
        'Евгин: привет [EOM}
        Борз: привет
        как дела? [EOM]'

        Output if messages is empty: ''
        """

        assert len(messages) <= self.context_size

        if messages:
            context = ""
            prev_message_author = None
            for message in messages:
                text = message.message.replace('@' + botname, '').strip()
                author = get_member(message.from_id).name
                if prev_message_author == author:
                    context += "\n" + text
                else:
                    prev_message_author = author
                    context += " [EOM]\n" + author + ": " + text

            context += " [EOM]\n" + "Славка" + ": "
            return context

        return ''
