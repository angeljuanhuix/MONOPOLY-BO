import json
from card import Card, build_card
import random

class Deck:
    """
    Representa una baralla de cartes (Chance o Community Chest)
    A l'inici es barregen les cartes i quan s'agafa una, es torna al piló per sota.
    Si és una carta per sortir de la presó, el jugador se la queda
    """
    _cards: list[Card]

    def __init__(self, path: str) -> None:
        """Carrega les targetes des d'un fitxer JSON"""

        with open(path) as file:
            data = json.load(file)
        self._cards = [build_card(card_data) for card_data in data]

    def cards(self) -> list[Card]:
        """Retorna una llista de les cartes del piló"""
        return self._cards

    def shuffle(self) -> None:
        """Barreja els elements de la llista (cartes)"""
        random.shuffle(self._cards)

    def return_get_out_of_jail_card(self, card: Card) -> None:
        """
        Torna la targeta de sortida de la presó al piló.
        Això passa quan un jugador cau en fallida o usa la carta
        """
        
        self._cards.append(card)

    def draw_card(self) -> Card:
        """Retorna la targeta que agafa el jugador i la retorna a sota del piló"""

        card = self._cards[0] #1a targeta
        self._cards = self._cards[1:] 
        card.set_deck(self) #assignem de quin piló prové la targeta (usat per tornar la carta de sortir de presó)

        if card.action() != "get_out_of_jail_card": #Tornem la targeta al piló menys si és per sortir de la presó
            self._cards.append(card)   

        return card
