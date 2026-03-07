from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player  #Perquè python no entri en un bucle infinit
    from tile import Property

class Strategy:
    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Decideix si el jugador compra o no una propietat"""
        
        raise NotImplementedError

        #QUAN ESTIGUEM MÉS AVANÇATS FER EL WANT_TO_BUILD_HOUSE, WANT_TO_MORTGAGE, WANT_TO_UNMORTGAGE
class Simple_Strategy(Strategy):
    """L'estratègia més simple: Si té prous diners, comprarà i mai construirà"""

    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Retorna un booleà si el jugador vol o no comprar"""
        return player.money() >= property.price