from __future__ import annotations
from typing import TYPE_CHECKING, Any

#from PROJECTE_MONOPOLY.CODIS.player import Player

if TYPE_CHECKING:
    from board import Board
    from player import Player


class Tile:
    """Base class for all board tiles."""

    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):    
        self._board = board
        self._position = position
        self._name = name
        self._tile_type = tile_type
        self._description = description
    
    def land_on(self, player: Player) -> None:
        """Handle what happens when a player lands on this tile."""
        pass #En principi, només passi perquè cada casella tindrà el seu land_on

    def type(self) -> str: 
        return self._tile_type
    
    def name(self) -> str: 
        return self._name
    
    def description(self) -> str: 
        return self._description
    
    def position(self) -> int: 
        return self._position
    
    def board(self) -> Board: 
        return self._board

class Property(Tile):

    def __init__(
        self,
        board: Board,
        position: int,
        name: str,
        tile_type: str,
        price: int,
        rent: int,
        mortgage: int,
        description: str,
    ): 
        super().__init__(board, position, name, tile_type, description)
        self._price = price
        self._rent = rent
        self._mortgage= mortgage
        self._owner = None

    @property
    def price(self) -> int:
        return self._price
    
    @property
    def rent(self) -> int:
        return self._rent
    
    @property
    def mortgage(self) -> int:
        return self._mortgage
    
    @property
    def owner(self) -> None|Player: #Quan no és de ningú tinc posat None, però quan és d'algú se li assigna el valor de Player
        return self._owner
    
    
    def availability(self) -> bool:
        """
        Retorna si aquella propietat es pot comprar
        o pertany a algú altre
        """
        return self._owner == None
    
    def buy(self, player: Player) -> None:
        """El jugador compra la propietat"""
        player.pay(self._price)
        player.add_property(self)
        self._owner = player
        print(f"{player.name()} ha comprat {self._name} per {self._price}$")
    
    def land_on(self, player: Player) -> None:
        if self.availability():
            if player.money() >= self._price:
                self.buy(player)
            else: print(f"{player.name()} no té prous diners per comprar {self._name}")
            
        else:
            if self._owner != player and self._owner is not None: #Tot i que ja sabem que l'owner no serà None, ho posem perquè el Pylance entengui que té propietari 100%
                player.pay(self._rent)
                self._owner.receive(self._rent)
                print(f"{player.name()} paga a {self._owner.name()} una quanitat de {self._rent}$")

        
class Street(Property):
    def __init__(
        self,
        board: Board,
        position: int,
        name: str,
        tile_type: str,
        color: str,
        price: int,
        rent: int,
        rent_with_color_set: int,
        rent_with_1_house: int,
        rent_with_2_houses: int,
        rent_with_3_houses: int,
        rent_with_4_houses: int,
        rent_with_hotel: int,
        house_cost: int,
        hotel_cost: int,
        mortgage: int,
    ): 
        super().__init__(board, position, name, tile_type, price, rent, mortgage, "")
        self._color = color
        self._rent_with_color_set = rent_with_color_set
        self._rent_with_1_house = rent_with_1_house
        self._rent_with_2_houses = rent_with_2_houses
        self._rent_with_3_houses = rent_with_3_houses
        self._rent_with_4_houses = rent_with_4_houses
        self._rent_with_hotel = rent_with_hotel
        self._house_cost = house_cost
        self._hotel_cost = hotel_cost

    @property #he posat això perquè sinó, no em surtien les caselles del color que toca
    def color(self) -> str:
        """Això fa que tile.color funcioni sense parèntesis"""
        return self._color
    
    #def rent_calculation(self) -> int:

class Station(Property):
    def __init__(
            self, 
            board: Board, 
            position: int, 
            name: str, 
            tile_type: str, 
            price: int, 
            rent: int, 
            mortgage: int, 
            rent_with_2_stations: int,
            rent_with_3_stations: int,
            rent_with_4_stations: int,

    ):
        super().__init__(board, position, name, tile_type, price, rent, mortgage, "")
        self._rent_with_2_stations = rent_with_2_stations
        self._rent_with_3_stations = rent_with_3_stations
        self._rent_with_4_stations = rent_with_4_stations

class Utility(Property):
    def __init__(
            self, 
            board: Board, 
            position: int, 
            name: str, 
            tile_type: str, 
            price: int, 
            mortgage: int, 
            description: str,
            rentMultiplier: int,
            rentMultiplierWithBoth: int,
    ):
        super().__init__(board, position, name, tile_type, price, 0, mortgage, description)
        self._rentMultiplier = rentMultiplier
        self._rentMultiplierWithBoth = rentMultiplierWithBoth

class chance(Tile):
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)

class community_chest(Tile):
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)

class tax(Tile):
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str,
        amount: int
    ):
        super().__init__(board, position, name, tile_type, description)
        self._amount = amount

class special(Tile):
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)


def build_tile(board: Board , data: dict[str, Any]) -> Tile:

    tile_type = data["type"]

    if tile_type == "property":
        return Street(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            color = data["color"],
            price = data["price"],
            rent = data["rent"],
            rent_with_color_set = data["rentWithColorSet"],
            rent_with_1_house = data["rentWith1House"],
            rent_with_2_houses = data["rentWith2Houses"],
            rent_with_3_houses = data["rentWith3Houses"],
            rent_with_4_houses = data["rentWith4Houses"],
            rent_with_hotel = data["rentWithHotel"],
            house_cost = data["houseCost"],
            hotel_cost = data["hotelCost"],
            mortgage = data["mortgage"])
    
    if tile_type == "station":
        return Station(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            price = data["price"],
            rent = data["rent"],
            mortgage = data["mortgage"],
            rent_with_2_stations = data["rentWith2Stations"],
            rent_with_3_stations = data["rentWith3Stations"],
            rent_with_4_stations = data["rentWith4Stations"],
            )
    if tile_type == "utility":
        return Utility(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            price = data["price"],
            mortgage = data["mortgage"],
            description = data["description"],
            rentMultiplier = data["rentMultiplier"],
            rentMultiplierWithBoth = data["rentMultiplierWithBoth"],
            )
    if tile_type == "chance":
        return chance(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            description = data["description"],
            )
    if tile_type == "community_chest":
        return community_chest(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            description = data["description"],
            )
    if tile_type == "tax":
        return tax(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            description = data["description"],
            amount = data["amount"],
            )
    else: #GO, Jail, Free Parking, Go to Jail
        return special(
            board = board,
            position = data["position"],
            name = data["name"],
            tile_type = data["type"],
            description = data["description"],
            )
    
    