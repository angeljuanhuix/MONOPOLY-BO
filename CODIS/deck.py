import json
from card import Card, build_card
import random

class Deck:

    _cards: list[Card]

    def __init__(self, path: str) -> None:
        with open(path) as file:
            data = json.load(file)
        self._cards = [build_card(card_data) for card_data in data]

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def draw_card(self) -> Card:
        card = self._cards[0] #Mirem la primera carta del piló
        self._cards = self._cards[1:] + [card] #La tornem a posar en el piló, però al final i eliminem el lloc on estava abans

        return card
