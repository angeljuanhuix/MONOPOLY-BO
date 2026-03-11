from __future__ import annotations
from typing import Any, TYPE_CHECKING

from const import GO_SALARY
from tile import Street
if TYPE_CHECKING:
    from player import Player

class Card:

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
    
    def id(self) -> int:
        return self._id
    
    def title(self) -> str:
        return self._title
    
    def description(self) -> str:
        return self._description
    
    def action(self) -> str:
        return self._action
    
    def execute(self, player: Player) -> None:
        raise NotImplementedError

class MoveToPosition(Card):
    def __init__(self, id: int, title: str, description: str, action: str, position: int):
        super().__init__(id, title, description, action)
        self._position = position

    def execute(self, player: Player) -> None:
        old_position = player.position()
        player.set_position(self._position)

        if self._position < old_position: #Significa que ha passat pel GO, ja que a partir del GO, comencen a comptar des del 0 les caselles
            player.receive(GO_SALARY)

        tile = player.board().tiles()[self._position]
        tile.land_on(player)
        
        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {self._position} (Cobra 200$ si passa pel GO)")

class MoveToNearestStation(Card):
    def __init__(self, id: int, title: str, description: str, action: str, rentMultiplier: int):
        super().__init__(id, title, description, action)
        self._rentMultiplier = rentMultiplier

    def _nearest_station_position(self, player: Player) -> int:

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

        if new_position < old_position: #Significa que ha passat pel GO, ja que a partir del GO, comencen a comptar des del 0 les caselles
            player.receive(GO_SALARY)
        
        tile = player.board().tiles()[new_position]
        tile.land_on(player, self._rentMultiplier)

        print(f"{player.name()} li ha tocat <{self._title}>. Posició actual: {new_position} (Cobra 200$ si passa pel GO)")

class MoveToNearestUtility(Card):
    def __init__(self, id: int, title: str, description: str, action: str, rentMultiplier: int):
        super().__init__(id, title, description, action)
        self._rentMultiplier = rentMultiplier

    def _nearest_utility_position(self, player: Player) -> int:

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
    def __init__(self, id: int, title: str, description: str, action: str, position: int):
        super().__init__(id, title, description, action)
        self._position = position

    def execute(self, player: Player) -> None:
        player.set_position(self._position)
        print(f"{player.name()} li ha tocat <{self._title}>. Va directament a la presó! (NO cobra 200$ si passa pel GO)")

class GetOutOfJailCard(Card):
    def __init__(self, id: int, title: str, description: str, action: str, keepCard: bool):
        super().__init__(id, title, description, action)
        self._keepCard = keepCard

    def execute(self, player: Player) -> None:
        player.add_get_out_of_jail_free_card()
        print(f"{player.name()} li ha tocat <{self._title}>. Té {player.get_out_of_jail_free_cards()} targeta/es de sortida de presó!")

class CollectMoney(Card):
    def __init__(self, id: int, title: str, description: str, action: str, amount: int):
        super().__init__(id, title, description, action)
        self._amount = amount

    def execute(self, player: Player) -> None:
        player.receive(self._amount)
        print(f"{player.name()} li ha tocat <{self._title}>. Rep {self._amount}$")

class PayMoney(Card):
    def __init__(self, id: int, title: str, description: str, action: str, amount: int):
        super().__init__(id, title, description, action)
        self._amount = amount

    def execute(self, player: Player) -> None:
        player.pay(self._amount)
        print(f"{player.name()} li ha tocat <{self._title}>. Paga {self._amount}$")

class PayPerProperty(Card):
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
    def __init__(self, id: int, title: str, description: str, action: str, amountPerPlayer: int):
        super().__init__(id, title, description, action)
        self._amountPerPlayer = amountPerPlayer

    def execute(self, player: Player) -> None:
        for other_player in player.board().players():
            if other_player != player and not other_player.broke():
                player.pay(self._amountPerPlayer)
                other_player.receive(self._amountPerPlayer)
                
        print(f"{player.name()} li ha tocat <{self._title}>. Paga {self._amountPerPlayer}$ a cada jugador")

class CollectFromPlayers(Card):
    def __init__(self, id: int, title: str, description: str, action: str, amountPerPlayer: int):
        super().__init__(id, title, description, action)
        self._amountPerPlayer = amountPerPlayer

    def execute(self, player: Player) -> None:
        for other_player in player.board().players():
            if other_player != player and not other_player.broke():
                other_player.pay(self._amountPerPlayer)
                player.receive(self._amountPerPlayer)
                
        print(f"{player.name()} li ha tocat <{self._title}>. Rep {self._amountPerPlayer}$ de cada jugador")

def build_card(data: dict[str, Any]) -> Card: 
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

