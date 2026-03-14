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
    
    def desire_of_mortgaging(self, player: Player, property: Property) -> bool:
        """Decideix si el jugador hipoteca o no una propietat"""
        raise NotImplementedError
    
    def desire_of_unmortgaging(self, player: Player, property: Property) -> bool:
        """Decideix si el jugador deshipoteca o no una propietat"""
        raise NotImplementedError

class Simple_Strategy(Strategy):
    """L'estratègia més simple: Comprarà propietat sempre que pugui, però mai construirà en carrers"""

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
    
    def desire_of_mortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol hipotecar propietats o no"""
        return False
    
    def desire_of_unmortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol deshipotecar propietats o no"""
        return False
    
class Smart_Strategy(Strategy):
    """Estratègia intel·ligent: compra sempre, construeix sempre que pot,
    hipoteca/ven si té menys de 300$ i deshipoteca si té més de 500$"""

    MINIMUM_MONEY = 100
    UNMORTGAGE_MONEY = 200

    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Retorna un booleà si el jugador pot o no comprar"""
        return player.money() >= property.price + self.MINIMUM_MONEY
    
    def desire_of_building_house(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol construir cases o no"""
        return  player.money() >= street.house_cost() + self.MINIMUM_MONEY
    
    def desire_of_building_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol construir hotels o no"""
        return player.money() >= street.hotel_cost() + self.MINIMUM_MONEY
    
    def desire_of_selling_house(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol vendre cases o no"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_selling_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol vendre hotels o no"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_mortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol hipotecar propietats o no"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_unmortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un booleà indicant si en aquesta estratègia es vol deshipotecar propietats o no"""
        return player.money() >= self.UNMORTGAGE_MONEY
