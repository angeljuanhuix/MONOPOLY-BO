from __future__ import annotations
from typing import TYPE_CHECKING, Any

from const import GO_SALARY, START_MONEY
from strategies import Strategy, Simple_Strategy, Smart_Strategy
if TYPE_CHECKING:
    from board import Board
    from tile import Property, Street
    from card import Card


class Player:
    """
    Representa un jugador del Monopoly.
    Es gestiona la posició, diners, propietats, decisions...
    """
    _board: Board
    _name: str
    _piece: str
    _color: str
    _index: int
    _position: int
    _money: int

    def __init__(self, board: Board, name: str, piece: str, color: str, index: int, strategy: Strategy): 
       """Inicialitza el jugador amb tots els atributs necessaris"""
       self._board = board 
       self._name = name 
       self._piece = piece 
       self._color = color 
       self._index = index
       self._strategy = strategy
       self._position = 0
       self._money = START_MONEY
       self._num_double = 0
       self._owned_properties: list[Property] = []
       self._get_out_of_jail_cards: list[Card] = []
       self._turns_in_prison = 0
       self._is_in_prison = False
       self._is_bankrupt = False
    
    def board(self) -> Board:
        """Retorna el taulell on es juga"""
        return self._board

    def name(self) -> str:
        """Retorna el nom del jugador"""
        return self._name
    
    # DECISIONS D'ESTRATÈGIA
    
    def strategy(self) -> Strategy:
        """Retorna l'estratègia assignada al jugador"""
        return self._strategy
    
    def wants_to_buy(self, property: Property) -> bool:
        """Segons l'estratègia, retorna si el jugador vol comprar una propietat"""
        return self._strategy.desire_of_buying(self, property)
    
    def wants_to_build_house(self, street: Street) -> bool:
        """Segons l'estratègia, retorna si el jugador vol construir una casa"""
        return self._strategy.desire_of_building_house(self, street)
    
    def wants_to_build_hotel(self, street: Street) -> bool:
        """Segons l'estratègia, retorna si el jugador vol construir un hotel"""
        return self._strategy.desire_of_building_hotel(self, street)
    
    def wants_to_sell_house(self, street: Street) -> bool:
        """Segons l'estratègia, retorna si el jugador vol vendre una casa"""
        return self._strategy.desire_of_selling_house(self, street)
    
    def wants_to_sell_hotel(self, street: Street) -> bool:
        """Segons l'estratègia, retorna si el jugador vol vendre un hotel"""
        return self._strategy.desire_of_selling_hotel(self, street)
    
    def wants_to_mortgage(self, property: Property) -> bool:
        """Segons l'estratègia, retorna si el jugador vol hipotecar una propietat"""
        return self._strategy.desire_of_mortgaging(self, property)
    
    def wants_to_unmortgage(self, property: Property) -> bool:
        """Segons l'estratègia, retorna si el jugador vol deshipotecar una propietat"""
        return self._strategy.desire_of_unmortgaging(self, property)

    # ATRIBUTS BÀSICS 

    @property
    def piece(self) -> str:
        """
        Retorna la peça del jugador (@property perquè sigui
        compatible amb el draw.py i no faci falta parèntesis)
        """
        return self._piece

    def color(self) -> str:
        """Retorna el color del jugador"""
        return self._color

    def index(self) -> int:
        """Retorna l'índex del jugador de la llista de jugadors"""
        return self._index
    
    # FALLIDA

    def is_bankrupt(self) -> bool:
        """Retorna un booleà indicar si està en fallida"""
        return self._is_bankrupt

    def go_bankrupt(self) -> None:
        """Marca el jugador que està en fallida i posa els diners a 0"""
        self._is_bankrupt = True
        self._money = 0

    def broke(self) -> bool:
        """Returna True si el jugador té diners negatius"""
        return self._money < 0

    # DINERS

    def money(self) -> int:
        """Retorna els diners que té el jugador"""
        return self._money

    def pay(self, amount: int) -> int:
        """Retorna els diners que té el jugador després de pagar"""
        self._money -= amount
        return self._money
    
    def receive(self, amount: int) -> int:
        """Retorna els diners que té el jugador després de rebre diners"""
        self._money += amount
        return self._money
    
    # POSICIÓ I MOVIMENTS

    def position(self) -> int:
        """Retorna la posició en què es troba el jugador"""
        return self._position
    
    def move(self, steps: int, num_tiles: int) -> None:
        """
        Mou el jugador un cert nombre de caselles endavant
        Si es passa pel GO, cobra 50$
        """
        

        self._position += steps 

        if self._position >= num_tiles:
            self._money += GO_SALARY
            self._position = self._position % num_tiles

    def set_position(self, new_position: int) -> None:
        """
        Teletransporta el jugador a la posició desitjada
        No es té en compte que passi pel GO
        """
        self._position = new_position

    # TARGETES DE PRESÓ
    
    def get_out_of_jail_cards(self) -> list[Card]:
        """Retorna la llista de targetes de sortida de presó que té el jugador"""
        return self._get_out_of_jail_cards
    
    def add_get_out_of_jail_free_card(self, card: Card) -> None:
        """Afegeix una carta de sortida de presó al jugador"""
        self._get_out_of_jail_cards.append(card)

    def get_out_of_jail_free_cards(self) -> int:
        """Retorna el nombre de targetes de sortida de presó que té el jugador"""
        return len(self._get_out_of_jail_cards)
    
    def use_get_out_of_jail_card(self) -> Card:
        """Retorna la carta usada de sortida de presó"""
        return self._get_out_of_jail_cards.pop()
    
    def clear_jail_cards(self) -> None:
        """Buida la llista de targetes de sortida de presó del jugador"""
        self._get_out_of_jail_cards = []

    # PRESÓ
    
    def add_turn_in_prison(self) -> None:
        """Incrementa el nombre de torns a la presó del jugador"""
        self._turns_in_prison  += 1

    def turns_in_prison(self) -> int:
        """Retorna els torns que porta a la presó el jugador"""
        return self._turns_in_prison
    
    def is_in_prison(self) -> bool:
        """Retorna un booleà indicant si és a la presó o no"""
        return self._is_in_prison
    
    def go_to_prison(self) -> None:
        """Envia el jugador a la presó sense cobrar quan passa pel GO"""
        self._is_in_prison = True
        self._position = 10 #Casella de la presó
        print(f"{self._name} ha anat a la presó! :(")

    def leave_prison(self) -> None:
        """
        Canvia l'estat del jugador quan surt de la 
        presó i reinicia el comptador de torns
        """
        self._is_in_prison = False
        self._turns_in_prison = 0
        print(f"{self._name} ha sortit de la presó! :)")

    # PROPIETATS

    def owned_properties(self) -> list[Property]:
        """Retorna la llista de propietats que té el jugador"""
        return self._owned_properties
    
    def add_property(self, property: Property) -> None:
        """Afegeix una propietat a la llista de propietats del jugador"""
        self._owned_properties.append(property)

    def clear_properties(self) -> None:
        """Buida la llista de propietats del jugador"""
        self._owned_properties = []

    

def build_player(board: Board, data: dict[str, Any], index: int) -> Player:
    """Build a Player from JSON-like dict with 'name', 'piece', and 'color' keys."""

    strategies: list[Strategy] = [Smart_Strategy(), Simple_Strategy(), Smart_Strategy(), Simple_Strategy()]
    return Player(board, data["name"], data["piece"], data["color"], index, strategies[index])
