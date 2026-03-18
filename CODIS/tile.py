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
    
    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Handle what happens when a player lands on this tile."""
        pass #Per defecte no fa res (GO, Free Parking, ...)

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
    """
    Casella que es pot comprar (carrer, estació o utility)
    Gestiona compra, lloguer, hipoteques i disponibilitat
    """

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
        Retorna True si aquella propietat no és de ningú
        """
        return self._owner == None
    
    def release_property(self) -> None:
        """Allibera la propietat (torna al banc, sense propietari ni hipoteca)"""
        
        self._owner = None
        self._is_mortgaged = False
    
    def buy(self, player: Player) -> None:
        """El jugador compra la propietat i és el propietari"""
        
        player.pay(self._price)
        player.add_property(self)
        self._owner = player
        print(f"{player.name()} ha comprat {self._name} per {self._price}$")

    def rent_calculation(self) -> int:
        """Retrona el lloguer bàsic. Cada tile té el seu"""
        
        return self._rent
    
    def can_mortgage(self) -> bool:
        """Retorna un True si la propietat no està hipotecada"""

        if self._is_mortgaged:
            return False
        return True
    
    def do_mortgage(self) -> None:
        """Hipoteca una propietat (el jugador rep el valor que té la hipoteca)"""
        assert self._owner is not None
        
        self._owner.receive(self._mortgage)
        self._is_mortgaged = True
        print(f"{self._owner.name()} ha hipotecat {self._name} i rep {self._mortgage}$")

    def can_unmortgage(self) -> bool:
        """Retornà True si la propietat està hipotecada i es pot deshipotecar"""
        
        return self._is_mortgaged
    
    def do_unmortgage(self) -> None:
        """Deshipoteca una propietat (el jugador paga 110% del valor de la hipoteca)"""
        
        assert self._owner is not None
        
        ten_percent = self._mortgage // 10
        self._owner.pay(self._mortgage + ten_percent)
        self._is_mortgaged = False
        print(f"{self._owner.name()} ha deshipotecat {self._name} pagant {self._mortgage + ten_percent}$")
    
    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Gestiona les accions que es poden fer quan un jugador hi cau"""
        
        if self._is_mortgaged: #Si està hipotecada no es fa res
            return None
        
        if self.availability(): # Si és lliure, jugador decideix si comprar-la segons l'estratègia
            if player.wants_to_buy(self): 
                self.buy(player)
            else: print(f"{player.name()} no té prous diners per comprar {self._name}")
            
        else:
            if self._owner != player and self._owner is not None: #owner is not None per evitar problemes amb el Pylance
                rent = self.rent_calculation() * rent_multiplier
                player.pay(rent)
                self._owner.receive(rent)
                print(f"{player.name()} paga a {self._owner.name()} una quantitat de {rent}$")

        
class Street(Property):
    """Gestió del carrer. Es poden construir cases i hotels (Si es té el Monopoli)"""
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

    @property 
    def color(self) -> str:
        """
        Retorna el color de la casella (@property perquè sigui
        compatible amb el draw.py i no faci falta parèntesis)
        """
        return self._color
    
    def house_cost(self) -> int:
        return self._house_cost

    def hotel_cost(self) -> int:
        return self._hotel_cost
    
    def has_monopoly(self) -> bool:
        """
        Retorna si el jugador té totes les propietats (carrers) del mateix color
        """
        assert self._owner is not None #Perquè Pylance no es queixi, 

        # Creem un diccionari constant del nombre de carrers que té cada color
        nombres_carrers: dict[str, int] = {"light_blue": 3, "pink": 3, "orange": 3, "red": 3, "yellow": 3, "green": 3, "brown": 2, "dark_blue": 2}
        
        # Suma per veure si té tots els carrers d'un color
        owned_same_color = sum(1 for property in self._owner.owned_properties() if isinstance(property, Street) and property.color == self._color)

        return owned_same_color == nombres_carrers[self._color]
    
    def can_build_house(self) -> bool:
        """
        Retorna True si es tenen els requisits per
        construir una casa en aquest carrer:
        - Tenir Monopoli
        - No té hotel
        - No té ja 4 cases
        - Construcció uniforme
        """

        if not self.has_monopoly(): 
            return False
        if self._hotels == 1:
            return False
        if self._houses == 4:
            return False
        
        assert self._owner is not None #Perquè no surti error en el Pylance

        #Construcció uniforme

        for street in self._owner.owned_properties():
            if isinstance(street, Street) and street.color == self._color and street != self:
                if street._houses < self._houses:
                    return False
        
        return True
    
    def build_house(self) -> None:
        """Es paga la casa i es construeix"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.pay(self._house_cost)
        self._houses += 1

        print(f"{self._owner.name()} ha construït una casa a {self._name} per {self._house_cost}$ (té {self._houses} casa/es)")

    def can_build_hotel(self) -> bool:
        """
        Retorna True si es compleixen els requisits 
        per construir un hotel en aquest carrer:
        - Té monopoli
        - Té exactametnt 4 cases
        - No té un hotel
        - Construcció uniforme
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
        """Es paga l'hotel i les 4 cases passen a ser un hotel"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.pay(self._hotel_cost)
        self._houses -= 4
        self._hotels = 1

        print(f"{self._owner.name()} ha construït un hotel a {self._name} per {self._hotel_cost}$")
    
    def can_sell_house(self) -> bool:
        """
        Retorna True si es tenen els requisits 
        per vendre una casa en aquest carrer:
        - Té monopoli
        - No té hotel
        - Té almenys una casa
        - Construcció uniforme 
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
        """El jugador ven una casa i rep la meitat del seu preu"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.receive(self._house_cost // 2) 
        self._houses -= 1

        print(f"{self._owner.name()} ha venut una casa a {self._name} (Li queda/en {self._houses} casa/es)")
    
    def can_sell_hotel(self) -> bool:
        """
        Retorna True si es tenen els requisits 
        per vendre un hotel en aquest carrer:
        - Té monopoli
        - Té hotel
        - Construcció uniforme 
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
        """El jugador ven un hotel i rep la meitat del seu preu"""

        assert self._owner is not None #Perquè no surti error en el Pylance

        self._owner.receive(self._hotel_cost // 2) 
        self._houses += 4
        self._hotels -= 1

        print(f"{self._owner.name()} ha venut un hotel a {self._name} (Ara té 4 cases)")

    def can_mortgage(self) -> bool:
        """
        Retornà un True si el carrer no té cases ni hotels
        i compleix els requisits per hipotecar-la
        """
        if self._houses > 0 or self._hotels == 1:
            return False
        
        return super().can_mortgage()

    def rent_calculation(self) -> int:
        """Retorna el preu del lloguer segons l'estat del carrer"""
        
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
    """Gestió de les estacions. Lloguer varia segons el nombre d'estacions"""
    
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
        """Retorna el preu de lloguer segons el nombre d'estacions que té el propietari"""
        
        assert self._owner is not None 
        
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
    """Gestió de les Utilities. (Lloguer: multiplicador x tirada daus)"""
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
        """
        Retorna el preu del lloguer segons la tirada dels daus: 4x si té 1 utility, 10x si en té 2.
        Tirada independent a la del moviment.
        """
        assert self._owner is not None 
        
        dice1, dice2 = self._board.current_dice() 
        num_utilities = sum(1 for property in self._owner.owned_properties() if isinstance(property, Utility))
        
        if num_utilities == 1:
            print(f"S'ha pagat {self._rentMultiplier * (dice1 + dice2)} perquè té 1 Utility")
            return self._rentMultiplier * (dice1 + dice2)
        else: #num_utilities == 2
            print(f"S'ha pagat {self._rentMultiplierWithBoth * (dice1 + dice2)} perquè té 2 Utility")
            return self._rentMultiplierWithBoth * (dice1 + dice2)
    
    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """
        Gestió quan es cau a una casella d'aquest tipus depenent 
        si es ve des d'una targeta o no (ja que canvia el multiplicador)
        """

        if self._is_mortgaged:
            return
        if self.availability():
            if player.wants_to_buy(self):
                self.buy(player)
        else:
            if self._owner != player and self._owner is not None:
                if rent_multiplier != 1: #Significa que el land_on s'ha cridat des d'una targeta chance
                    dice1, dice2 = self._board.current_dice()
                    rent = rent_multiplier * (dice1 + dice2)
                else: # Càlcul normal
                    rent = self.rent_calculation()
                player.pay(rent)
                self._owner.receive(rent)
                print(f"{player.name()} paga {rent}$ a {self._owner.name()}")
        

class chance(Tile):
    """Gestió de casella Chance"""
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)

    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Si es cau en aquesta casella, el jugador agafa una carta i fa el que digui"""
        card = self._board.chance_deck().draw_card()
        print(f"{player.name()} agafa una chance card")
        card.execute(player)

class community_chest(Tile):
    """Gestió de casella Community_chest"""
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)
    
    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Si es cau en aquesta casella, el jugador agafa una carta i fa el que digui"""
        card = self._board.community_chest_deck().draw_card()
        print(f"{player.name()} agafa una community_chest card")
        card.execute(player)
       

class tax(Tile):
    """Gestió de casella de Tax"""
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

    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Si es cau en aquesta casella, el jugador paga el que digui la casella"""
        player.pay(self._amount)
        print(f"{player.name()} paga {self._amount}$ d'impostos: {self._name}")

class special(Tile):
    """Gestió de caselles especials (GO, Just visiting, Free Parking, Go to Jail)"""
    def __init__(
        self, 
        board: Board, 
        position: int, 
        name: str, 
        tile_type: str, 
        description: str
    ):
        super().__init__(board, position, name, tile_type, description)

    def land_on(self, player: Player, rent_multiplier: int = 1) -> None:
        """Si es cau en una casella d'aquest tipus, només Go to Jail té execució"""
        if self._name == "Go To Jail":
            player.go_to_prison()
            print(f"{player.name()} ha caigut a la casella d'anar a la presó!!!")

def build_tile(board: Board , data: dict[str, Any]) -> Tile:
    """Build a tile from JSON"""
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
    
    