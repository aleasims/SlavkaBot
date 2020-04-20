import random
import logging
from typing import Tuple, Iterable

from slavkabot import get_member, Member
from slavkabot.ChatBotAI import ChatBotAI

logger = logging.getLogger(__name__)


class Slavka:
    def __init__(self, phrases='slavkabot/phrases.txt'):
        with open(phrases, 'r', encoding='utf-8') as f:
            self.phrases = [phrase.strip() for phrase in f.readlines()]

        try:
            self.chat_bot_ai = ChatBotAI()
            self.name = get_member('Славка').name
            self.model_loaded = True
            logger.info('ChatBotAI loaded')
        except Exception as e:
            logger.warn(f'Error during ChatBotAI initialization: {e}')
            logger.warn(f'Using random sampling instead ChatBotAI')
            self.model_loaded = False

    def greeting(self) -> str:
        return "Батя в здании!"

    def welcome(self) -> str:
        return "Добро пожаловать в хату!"

    def random_phrase(self) -> str:
        """Returns random phrase from provied in `self.phrases`."""
        return random.choice(self.phrases)

    def respond(self, context: Iterable[Tuple[Member, str]]) -> str:
        """Respond to a message with provided context.

        Returns:
            Text of response message. If generative model loaded,
            returns sampled result. Otherwise returns random phrase.
        """

        if self.model_loaded:
            inp_text = self.to_string(context)
            logger.debug(f'Feeding context: {repr(inp_text)}')

            out_text = self.chat_bot_ai.respond(inp_text)
            logger.debug(f'Generated response: {repr(out_text)}')

            for EOM in self.chat_bot_ai.EOM:
                out_text = out_text.split(EOM)[0]
            return out_text

        return self.random_phrase()

    def to_string(self, messages: Iterable[Tuple[Member, str]]) -> str:
        """Convert sequence of messages into string.

        Example:
            'Евгин: привет[EOM]
            Борз: привет
            как дела?[EOM]
            Славка: '

        Return `'Славка: '`, if messages is empty
        """

        lines = []
        prev_name = ''
        for i, (member, text) in enumerate(messages):
            if member.name != prev_name:
                if i > 0:
                    lines[i - 1] += self.chat_bot_ai.EOM
                prev_name = member.name
                text = ' '.join(filter(lambda part: not part.startswith('@'),
                                       text.split()))
                message = '{author}: {text}'.format(author=member.name,
                                                    text=text)
            else:
                message = text
            lines.append(message)

        lines.append(self.name + ': ')
        return '\n'.join(lines)
