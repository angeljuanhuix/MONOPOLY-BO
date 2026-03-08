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
        pass #Utilitzem aquest land_on com a pare de les altres, però com les propietats
            # i les tax, special, community and chance no tenen res en comú, no hi podem posar res aquí

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
        self._is_mortgaged = False

    @property
    def is_mortgaged(self) -> bool:
        return self._is_mortgaged

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

    def rent_calculation(self) -> int:
        """Mètode que retornà el preu de lloguer depenent de la propietat
        gràcies a la seva herència"""
        return self._rent
    
    def can_mortgage(self) -> bool:
        """
        Retornà un booleà indicant True si compleix els
        requisits per hipotecar el carrer i False pel contrari
        """
        if self._is_mortgaged:
            return False
        return True
    
    def do_mortgage(self) -> None:
        """Hipoteca un carrer"""
        assert self._owner is not None
        
        self._owner.receive(self._mortgage)
        self._is_mortgaged = True
        print(f"{self._owner.name()} ha hipotecat {self._name} i rep {self._mortgage}$")

    def can_unmortgage(self) -> bool:
        """
        Retornà un booleà indicant True si compleix els
        requisits per deshipotecar el carrer i False pel contrari
        """
        return self._is_mortgaged
    
    def do_unmortgage(self) -> None:
        """Deshipoteca un carrer"""
        assert self._owner is not None
        ten_percent = self._mortgage // 10
        self._owner.pay(self._mortgage + ten_percent)
        self._is_mortgaged = False
        print(f"{self._owner.name()} ha deshipotecat {self._name} pagant {self._mortgage + ten_percent}$")
    
    def land_on(self, player: Player) -> None:
        """Gestiona el que s'ha de fer quan un jugador cau en una propietat"""
        if self._is_mortgaged: #Si la casella està hipotecada, no cal que executi res més
            return None
        
        if self.availability():
            if player.wants_to_buy(self): #Seguim l'estratègia
                self.buy(player)
            else: print(f"{player.name()} no té prous diners per comprar {self._name}")
            
        else:
            if self._owner != player and self._owner is not None: #Tot i que ja sabem que l'owner no serà None, ho posem perquè el Pylance entengui que té propietari 100%
                rent = self.rent_calculation()
                player.pay(rent)
                self._owner.receive(rent)
                print(f"{player.name()} paga a {self._owner.name()} una quantitat de {rent}$")

        
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
        self._houses = 0
        self._hotels = 0
    
    @property
    def houses(self) -> int:
        return self._houses
    
    @property
    def hotels(self) -> int:
        return self._hotels

    @property #he posat això perquè sinó, no em surtien les caselles del color que toca
    def color(self) -> str:
        """Això fa que tile.color funcioni sense parèntesis"""
        return self._color
    
    #Creem un diccionari constant del nombre de carrers que té cada color
    nombres_carrers: dict[str, int] = {"light_blue": 3, "pink": 3, "orange": 3, "red": 3, "yellow": 3, "green": 3, "brown": 2, "dark_blue": 2}
    
    def has_monopoly(self) -> bool:
        """
        Retorna si el jugador té totes les propietat del mateix color
        """
        assert self._owner is not None #Perquè Pylance no es queixi, 
        #però nosaltres sabem que si arribem a aquest punt, l'owner sempre tindrà mínim una propietat
        
        #isinstance perquè el programa miri si és street i sàpiga que ho és i així no tenir problemes amb el property.color
        owned_same_color = sum(1 for property in self._owner.owned_properties() if isinstance(property, Street) and property.color == self._color)

        return owned_same_color == self.nombres_carrers[self._color]
    
    def can_build_house(self) -> bool:
        """
        Comprova si es tenen els requisits per
        construir una casa en aquest carrer
        """
        if not self.has_monopoly():
            return False
        if self._hotels == 1:
            return False
        if self._houses == 4:
            return False
        
        assert self._owner is not None #Perquè no surti error en el Pylance

        for street in self._owner.owned_properties():
            if isinstance(street, Street) and street.color == self._color and street != self:
                if street._houses < self._houses:
                    return False
        return True
    
    def build_house(self) -> None:
        """Construeix una casa"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.pay(self._house_cost)
        self._houses += 1

        print(f"{self._owner.name()} ha construït una casa a {self._name} per {self._house_cost}$ (té {self._houses} casa/es)")

    def can_build_hotel(self) -> bool:
        """
        Comprova si es compleixen els requisits 
        per construir un hotel en aquest carrer
        """
        if not self.has_monopoly():
            return False
        if self._hotels == 1:
            return False
        if self._houses != 4:
            return False
        
        assert self._owner is not None #Perquè no surti error en el Pylance

        for street in self._owner.owned_properties():
            if isinstance(street, Street) and street.color == self._color and street != self:
                if street._houses < 4 and street._hotels != 1:
                    return False
        return True
    
    def build_hotel(self) -> None:
        """Construeix un hotel"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.pay(self._hotel_cost)
        self._houses -= 4
        self._hotels = 1

        print(f"{self._owner.name()} ha construït un hotel a {self._name} per {self._hotel_cost}$")
    
    def can_sell_house(self) -> bool:
        """
        Comprova si es tenen els requisits 
        per vendre una casa en aquest carrer
        """
        if not self.has_monopoly():
            return False
        if self._hotels == 1:
            return False
        if self._houses == 0:
            return False
        
        assert self._owner is not None #Perquè no surti error en el Pylance

        for street in self._owner.owned_properties():
            if isinstance(street, Street) and street.color == self._color and street != self:
                if street._hotels == 1:
                    return False
                
                if street._houses > self._houses:
                    return False
                
        return True
    
    def sell_house(self) -> None:
        """Ven una casa"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.receive(self._house_cost // 2) #Li retornen la meitat del preu d'una casa
        self._houses -= 1

        print(f"{self._owner.name()} ha venut una casa a {self._name} (Li queda/en {self._houses} casa/es)")
    
    def can_sell_hotel(self) -> bool:
        """
        Comprova si es tenen els requisits 
        per vendre un hotel en aquest carrer
        """
        if not self.has_monopoly():
            return False
        if self._hotels != 1:
            return False          
        
        assert self._owner is not None #Perquè no surti error en el Pylance

        for street in self._owner.owned_properties():
            if isinstance(street, Street) and street.color == self._color and street != self:
                if street._hotels != 1 and street._houses < 4:
                    return False
                
        return True
    
    def sell_hotel(self) -> None:
        """Ven un hotel"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.receive(self._hotel_cost // 2) #Li retornen la meitat del preu de l'hotel
        self._houses += 4
        self._hotels -= 1

        print(f"{self._owner.name()} ha venut un hotel a {self._name} (Ara té 4 cases)")

    def can_mortgage(self) -> bool:
        """
        Retornà un booleà indicant True si compleix els
        requisits per hipotecar el carrer i False pel contrari
        """
        if self._houses > 0 or self._hotels == 1:
            return False
        
        return super().can_mortgage()

    def rent_calculation(self) -> int:
        """Calcula el lloguer d'aquell carrer"""
        if self._hotels == 1:
            return self._rent_with_hotel
        elif self._houses == 4:
            return self._rent_with_4_houses
        elif self._houses == 3:
            return self._rent_with_3_houses
        elif self._houses == 2:
            return self._rent_with_2_houses
        elif self._houses == 1:
            return self._rent_with_1_house
        elif self.has_monopoly():
            return self._rent_with_color_set
        else:
            return self._rent
            
                
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

    def rent_calculation(self) -> int:

        assert self._owner is not None #Comprovem que la casella té propietari, tot i que sabem que 100% en tindrà arribat a aquest punt
        num_stations = sum(1 for property in self._owner.owned_properties() if isinstance(property, Station))

        if num_stations == 1:
            print(f"S'ha pagat {self._rent} perquè té 1 estació")
            return self._rent
        elif num_stations == 2:
            print(f"S'ha pagat {self._rent_with_2_stations} perquè té 2 estacions")
            return self._rent_with_2_stations
        elif num_stations == 3:
            print(f"S'ha pagat {self._rent_with_3_stations} perquè té 3 estacions")
            return self._rent_with_3_stations
        else: #num_stations == 4
            print(f"S'ha pagat {self._rent_with_4_stations} perquè té 4 estacions")
            return self._rent_with_4_stations
        

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
    
    def rent_calculation(self) -> int:
        assert self._owner is not None #Per evitar que surti error del Pylance
        
        dice1, dice2 = self._board.current_dice() #Tornem a tirar els daus
        num_utilities = sum(1 for property in self._owner.owned_properties() if isinstance(property, Utility))
        
        if num_utilities == 1:
            print(f"S'ha pagat {self._rentMultiplier * (dice1 + dice2)} perquè té 1 Utility")
            return self._rentMultiplier * (dice1 + dice2)
        else: #num_utilities == 2
            print(f"S'ha pagat {self._rentMultiplierWithBoth * (dice1 + dice2)} perquè té 2 Utility")
            return self._rentMultiplierWithBoth * (dice1 + dice2)
        

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
    
    