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

    def return_get_out_of_jail_card(self, card: Card) -> None:
        self._cards.append(card)

    def draw_card(self) -> Card:
        card = self._cards[0] #Mirem la primera carta del piló
        self._cards = self._cards[1:] #Queden totes les cartes menys la que hem agafat
        card.set_deck(self) #assignem de quin piló ve la carta (usat per tornar la carta de sortir de presó)

        if card.action() != "get_out_of_jail_card": #Tornem carta al piló menys si és per sortir de la presó que la guardem
            self._cards.append(card)   

        return card
