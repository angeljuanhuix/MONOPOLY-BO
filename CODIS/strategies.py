from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player  #Perquè python no entri en un bucle infinit
    from tile import Property, Street

class Strategy:
    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Decideix si el jugador compra o no una propietat"""
        
        raise NotImplementedError

    def desire_of_building_house(self, player: Player, street: Street) -> bool:
        """Decideix si el jugador construeix o no una casa"""
        raise NotImplementedError
    
    def desire_of_building_hotel(self, player: Player, street: Street) -> bool:
        """Decideix si el jugador construeix o no un hotel"""
        raise NotImplementedError
    
    def desire_of_selling_house(self, player: Player, street: Street) -> bool:
        """Decideix si el jugador ven o no una casa"""
        raise NotImplementedError
    
    def desire_of_selling_hotel(self, player: Player, street: Street) -> bool:
        """Decideix si el jugador ven o no un hotel"""
        raise NotImplementedError
        #QUAN ESTIGUEM MÉS AVANÇATS FER EL WANT_TO_BUILD_HOUSE, WANT_TO_MORTGAGE, WANT_TO_UNMORTGAGE

class Simple_Strategy(Strategy):
    """L'estratègia més simple: Si té prous diners, comprarà carrers, però mai construirà"""

    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Retorna un booleà si el jugador pot o no comprar"""
        return player.money() >= property.price
    
    def desire_of_building_house(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol construir cases o no"""
        return False 
    
    def desire_of_building_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol construir hotels o no"""
        return False
    
    def desire_of_selling_house(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol vendre cases o no"""
        return False
    
    def desire_of_selling_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol vendre hotels o no"""
        return False
