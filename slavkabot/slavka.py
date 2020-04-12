import random


class Slavka:
    def __init__(self, phrases='slavkabot/phrases.txt'):
        with open(phrases, 'r', encoding='utf-8') as f:
            self.phrases = [phrase.strip() for phrase in f.readlines()]

    def greeting(self):
        return "Батя в здании!"

    def welcome(self):
        return "Добро пожаловать в хату!"

    def random_phrase(self):
        return random.choice(self.phrases)
