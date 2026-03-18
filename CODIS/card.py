from __future__ import annotations
from typing import Any, TYPE_CHECKING

from const import GO_SALARY
from tile import Street
if TYPE_CHECKING:
    from player import Player
    from deck import Deck

class Card:
    """
    Classe base per a les cartes del joc. 
    Cada subclasse tindrà el seu propi execute()
    """
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        action: str,
    ) -> None: 
        self._id = id
        self._title = title
        self._description = description
        self._action = action
        self._deck = None # S'assignarà quan es robi de la baralla
    
    def id(self) -> int:
        """Retorna l'identificador de la targeta"""
        return self._id
    
    def title(self) -> str:
        """Retorna el títol de la targeta"""
        return self._title
    
    def description(self) -> str:
        """Retorna la descripció de la targeta"""
        return self._description
    
    def action(self) -> str:
        """Retorna l'acció de la targeta"""
        return self._action
    
    def set_deck(self, deck: Deck) -> None:
        """Assinga la baralla d'on prové la carta"""
        self._deck = deck

    def deck(self) -> Deck:
        """Retorna la baralla de la carta"""
        assert self._deck is not None #Sabem que sempre que s'utilitza això mai és None
        return self._deck
    
    def execute(self, player: Player) -> None:
        """Executa l'acció de cada targeta. Cada subclasse té un execute()"""
        raise NotImplementedError

class MoveToPosition(Card):
    """Mou el jugador a una casella concreta. (Cobra 50$ si passa pel GO)"""
    
    def __init__(self, id: int, title: str, description: str, action: str, position: int):
        super().__init__(id, title, description, action)
        self._position = position

    def execute(self, player: Player) -> None:
        old_position = player.position()
        player.set_position(self._position)

        if self._position < old_position: 
            player.receive(GO_SALARY)

        tile = player.board().tiles()[self._position]
        tile.land_on(player)
        
        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {self._position} (Cobra 200$ si passa pel GO)")

class MoveToNearestStation(Card):
    """Mou el jugador a la propera estació. (Si té propietari, paga el doble de lloguer)"""
    
    def __init__(self, id: int, title: str, description: str, action: str, rentMultiplier: int):
        super().__init__(id, title, description, action)
        self._rentMultiplier = rentMultiplier

    def _nearest_station_position(self, player: Player) -> int:
        """
        Retorna la posició de l'estació més propera
        respecte la posició del jugador
        """

        #Posicions de les estacions: 5, 15, 25, 35
        
        if 35 < player.position() or player.position() < 5:
            return 5
        
        if 5 < player.position() < 15:
            return 15
        
        if 15 < player.position() < 25:
            return 25
        
        return 35

    def execute(self, player: Player) -> None:
        
        new_position = self._nearest_station_position(player)
        old_position = player.position()
        player.set_position(new_position)

        if new_position < old_position: 
            player.receive(GO_SALARY)
        
        tile = player.board().tiles()[new_position]
        tile.land_on(player, self._rentMultiplier)

        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {new_position} (Cobra 200$ si passa pel GO)")

class MoveToNearestUtility(Card):
    """
    Mou el jugador a la propera Utility. (Si té propietari, x10 la suma 
    dels daus, independentment de quantes utilities tingui el propietari)
    """
    
    def __init__(self, id: int, title: str, description: str, action: str, rentMultiplier: int):
        super().__init__(id, title, description, action)
        self._rentMultiplier = rentMultiplier

    def _nearest_utility_position(self, player: Player) -> int:
        """
        Retorna la posició de l'utility més propera
        respecte la posició del jugador
        """
        #Posicions de les utilities: 12, 28
        
        if 12 < player.position() < 28:
            return 28
        
        return 12

    def execute(self, player: Player) -> None:
        
        new_position = self._nearest_utility_position(player)
        old_position = player.position()
        player.set_position(new_position)

        if new_position < old_position: #Significa que ha passat pel GO, ja que a partir del GO, comencen a comptar des del 0 les caselles
            player.receive(GO_SALARY)
        
        tile = player.board().tiles()[new_position]
        tile.land_on(player, self._rentMultiplier)

        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {new_position} (Cobra 200$ si passa pel GO)")

class MoveBackSpaces(Card):
    """
    Mou el jugadors tantes caselles 
    endarrere com indiqui la carta
    """
    
    def __init__(self, id: int, title: str, description: str, action: str, spaces: int):
        super().__init__(id, title, description, action)
        self._spaces = spaces

    def execute(self, player: Player) -> None:
        new_position = player.position() - self._spaces
        player.set_position(new_position)

        tile = player.board().tiles()[new_position]
        tile.land_on(player)

        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {new_position}")
    
class GoToJail(Card):
    """Envia el jugador a la presó sense cobrar el GO_SALARY"""
    
    def __init__(self, id: int, title: str, description: str, action: str, position: int):
        super().__init__(id, title, description, action)
        self._position = position

    def execute(self, player: Player) -> None:
        player.go_to_prison()
        print(f"{player.name()} li ha tocat <{self._title}>. Va directament a la presó! (NO cobra 200$ si passa pel GO)")

class GetOutOfJailCard(Card):
    """
    Carta que guarda el jugador i es pot utilitzar per sortir
    de la presó sense complir els requirements per defecte (dobles, o esperar 3 torns)
    """
    
    def __init__(self, id: int, title: str, description: str, action: str, keepCard: bool):
        super().__init__(id, title, description, action)
        self._keepCard = keepCard

    def execute(self, player: Player) -> None:
        player.add_get_out_of_jail_free_card(self)
        print(f"{player.name()} li ha tocat <{self._title}>. Té {player.get_out_of_jail_free_cards()} targeta/es de sortida de presó!")

class CollectMoney(Card):
    """El jugador rep la quantitat de diners que indica la carta"""
    
    def __init__(self, id: int, title: str, description: str, action: str, amount: int):
        super().__init__(id, title, description, action)
        self._amount = amount

    def execute(self, player: Player) -> None:
        player.receive(self._amount)
        print(f"{player.name()} li ha tocat <{self._title}>. Rep {self._amount}$")

class PayMoney(Card):
    """El jugador paga la quantitat de diners que indica la carta"""
    
    def __init__(self, id: int, title: str, description: str, action: str, amount: int):
        super().__init__(id, title, description, action)
        self._amount = amount

    def execute(self, player: Player) -> None:
        player.pay(self._amount)
        print(f"{player.name()} li ha tocat <{self._title}>. Paga {self._amount}$")

class PayPerProperty(Card):
    """El jugador paga certa quantitat de diners per cada casa i hotel que té construïts"""
    
    def __init__(self, id: int, title: str, description: str, action: str, amountPerHouse: int, amountPerHotel: int):
        super().__init__(id, title, description, action)
        self._amountPerHouse = amountPerHouse
        self._amountPerHotel = amountPerHotel
    
    def execute(self, player: Player) -> None:
        total_hotels = 0
        total_houses = 0
        for propietat in player.owned_properties():
            if isinstance(propietat, Street):
                total_hotels += propietat.hotels
                total_houses += propietat.houses
        
        total_payment = total_hotels * self._amountPerHotel + total_houses * self._amountPerHouse

        player.pay(total_payment)
        print(f"{player.name()} li ha tocat <{self._title}>. Paga {total_payment}$ ({self._amountPerHouse} per casa i {self._amountPerHotel} per hotel)")

class PayEachPlayer(Card):
    """El jugador paga una certa quantitat de diners a cada jugador actiu"""
    
    def __init__(self, id: int, title: str, description: str, action: str, amountPerPlayer: int):
        super().__init__(id, title, description, action)
        self._amountPerPlayer = amountPerPlayer

    def execute(self, player: Player) -> None:
        for other_player in player.board().players():
            if other_player != player and not other_player.is_bankrupt():
                player.pay(self._amountPerPlayer)
                other_player.receive(self._amountPerPlayer)
                
        print(f"{player.name()} li ha tocat <{self._title}>. Paga {self._amountPerPlayer}$ a cada jugador")

class CollectFromPlayers(Card):
    """El jugador rep una certa quantitat de diners dels altres jugadors actius"""
    
    def __init__(self, id: int, title: str, description: str, action: str, amountPerPlayer: int):
        super().__init__(id, title, description, action)
        self._amountPerPlayer = amountPerPlayer

    def execute(self, player: Player) -> None:
        for other_player in player.board().players():
            if other_player != player and not other_player.is_bankrupt():
                other_player.pay(self._amountPerPlayer)
                player.receive(self._amountPerPlayer)
                
        print(f"{player.name()} li ha tocat <{self._title}>. Rep {self._amountPerPlayer}$ de cada jugador")

def build_card(data: dict[str, Any]) -> Card: 
    """Construeix la classe adequada per a cada tipus de carta a traves dels fitxers JSON"""
    action = data["action"]
    
    if action == "move_to_position":
        return MoveToPosition(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            position = data["position"]
        )
    if action == "move_to_nearest_station":
        return MoveToNearestStation(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            rentMultiplier = data["rentMultiplier"]
        )
    if action == "move_to_nearest_utility":
        return MoveToNearestUtility(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            rentMultiplier = data["rentMultiplier"]
        )
    if action == "move_back_spaces":
        return MoveBackSpaces(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            spaces = data["spaces"]
        )
    
    if action == "go_to_jail":
        return GoToJail(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            position = data["position"]
        )
    
    if action == "get_out_of_jail_card":
        return GetOutOfJailCard(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            keepCard = data["keepCard"]
        )

    if action == "collect_money":
        return CollectMoney(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            amount = data["amount"]
        )
    if action == "pay_money":
        return PayMoney(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            amount = data["amount"]
        )
    
    if action == "pay_per_property":
        return PayPerProperty(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            amountPerHouse = data["amountPerHouse"],
            amountPerHotel = data["amountPerHotel"]
        )
    if action == "pay_each_player":
        return PayEachPlayer(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            amountPerPlayer = data["amountPerPlayer"]
        )
    else:  # action == "collect_from_players"
        return CollectFromPlayers(
            id = data["id"],
            title = data["title"],
            description = data["description"],
            action = data["action"],
            amountPerPlayer = data["amountPerPlayer"]
        )

