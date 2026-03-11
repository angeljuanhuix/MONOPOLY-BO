from __future__ import annotations
from typing import TYPE_CHECKING, Any

from const import GO_SALARY
from strategies import Strategy, Simple_Strategy
if TYPE_CHECKING:
    from board import Board
    from tile import Property, Street


class Player:
    _board: Board
    _name: str
    _piece: str
    _color: str
    _index: int
    _position: int
    _money: int

    def __init__(self, board: Board, name: str, piece: str, color: str, index: int, strategy: Strategy): 
       self._board = board 
       self._name = name 
       self._piece = piece 
       self._color = color 
       self._index = index
       self._strategy = strategy
       self._position = 0
       self._money = 1500
       self._num_double = 0
       self._owned_properties: list[Property] = []
       self._get_out_of_jail_free_cards = 0

    def num_double(self) -> int:
        """Comptador de dobles en x tirada"""
        return self._num_double
    
    def board(self) -> Board:
        return self._board

    def name(self) -> str:
        return self._name
    
    #BOOLEANS D'ESTRATÈGIA
    
    def strategy(self) -> Strategy:
        return self._strategy
    
    def wants_to_buy(self, property: Property) -> bool:
        """
        Segons l'estrategia, es decideix si el jugador
        vol comprar una propietat o no
        """
        return self._strategy.desire_of_buying(self, property)
    
    def wants_to_build_house(self, street: Street) -> bool:
        """Segons l'estratègia del jugador, es retorna si
        vol construir una casa o no"""
        return self._strategy.desire_of_building_house(self, street)
    
    def wants_to_build_hotel(self, street: Street) -> bool:
        """Segons l'estratègia del jugador, es retorna si vol 
        construir un hotel o no"""
        return self._strategy.desire_of_building_hotel(self, street)
    
    def wants_to_sell_house(self, street: Street) -> bool:
        """Segons l'estratègia del jugador, es retorna si vol 
        vendre una casa o no"""
        return self._strategy.desire_of_selling_house(self, street)
    
    def wants_to_mortgage(self, property: Property) -> bool:
        """Segons l'estratègia del jugador, es retorna si vol 
        hipotecar una propietat o no"""
        return self._strategy.desire_of_mortgaging(self, property)
    
    def wants_to_unmortgage(self, property: Property) -> bool:
        """Segons l'estratègia del jugador, es retorna si vol 
        deshipotecar una propietat o no"""
        return self._strategy.desire_of_unmortgaging(self, property)

    @property
    def piece(self) -> str:
        return self._piece

    def color(self) -> str:
        return self._color

    def index(self) -> int:
        return self._index

    def broke(self) -> bool:
        """Return True if the player has negative money."""
        return self._money < 0

    def money(self) -> int:
        return self._money

    def position(self) -> int:
        return self._position
    
    def add_get_out_of_jail_free_card(self) -> None:
        self._get_out_of_jail_free_cards += 1

    def get_out_of_jail_free_cards(self) -> int:
        return self._get_out_of_jail_free_cards

    def turns_in_prison(self) -> int:
        return 0

    def owned_properties(self) -> list[Property]:
        return self._owned_properties
    
    def add_property(self, property: Property) -> None:
        self._owned_properties.append(property)
    
    def pay(self, amount: int) -> int:
        self._money -= amount
        return self._money
    
    def receive(self, amount: int) -> int:
        self._money += amount
        return self._money

    def move(self, steps: int, num_tiles: int) -> None:
        """Mou el jugador un cert nombre de caselles (steps)"""
        #Actualitzem la posició del jugador quan es mou 

        self._position += steps 

        #Si passa per la casella de sortida, s'haurà de sumar-li 200$

        if self._position >= num_tiles:
            self._money += GO_SALARY
            self._position = self._position % num_tiles
        #("%" s'ha utilitzat perquè la posició sempre estigui dins del límit de caselles del taulell)

    def set_position(self, new_position: int) -> None:
        """Teletransporta el jugador a la posició desitjada"""
        self._position = new_position

def build_player(board: Board, data: dict[str, Any], index: int) -> Player:
    """Build a Player from JSON-like dict with 'name', 'piece', and 'color' keys."""

    strategies = [Simple_Strategy(), Simple_Strategy(), Simple_Strategy(), Simple_Strategy()]
    return Player(board, data["name"], data["piece"], data["color"], index, strategies[index])
