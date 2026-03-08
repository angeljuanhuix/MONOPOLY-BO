from __future__ import annotations
from typing import Any, TYPE_CHECKING
from const import GO_SALARY
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
        
        #PENSAR DE QUINA MANERA FER EL LAND_ON D'AQUESTA CASELLA

        
    


def build_card(data: dict[str, Any]) -> Card: 
    return Card(
        id = data["id"],
        title = data["title"],
        description = data["description"],
        action = data["action"],
    )

