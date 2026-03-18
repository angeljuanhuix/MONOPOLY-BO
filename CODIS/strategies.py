from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: #Perquè python no entri en un bucle infinit
    from player import Player  
    from tile import Property, Street

#raise NotImplementedError -> Per si de cas que algun jugador
#no se li hagi implementat correctament l'estratègia
class Strategy:
    """
    Classe base per a les estratègies on totes les funcions 
    un booleà indicant si aquell jugador vol fer aquella acció o no.
    """
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
    """
    L'estratègia més simple: Comprarà una propietat sempre que pugui, 
    però mai construirà ni cases ni hotels ni tampoc hipotecarà
    """

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
    """Estratègia intel·ligent: Compra i construeix sempre que pugui mantenint
    un mínim de diners (MINIMUM_MONEY). Hipoteca i ven si els diners
    baixen del mínim, i deshipoteca quan té prous diners per fer-ho (UNMORTGAGE_MONEY)."""

    MINIMUM_MONEY = 150 # Coixí mínim que s'ha de tenir sempre

    UNMORTGAGE_MONEY = 300 # Diners necessaris per deshipotecar

    def desire_of_buying(self, player: Player, property: Property) -> bool:
        """Retorna un True si després de comprar li queden almenys MINIMUM_MONEY"""
        return player.money() >= property.price + self.MINIMUM_MONEY
    
    def desire_of_building_house(self, player: Player, street: Street) -> bool:
        """Retorna un True si després de construir una casa li queden almenys MINIMUM_MONEY."""
        return  player.money() >= street.house_cost() + self.MINIMUM_MONEY
    
    def desire_of_building_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un True si després de construir un hotel li queden almenys MINIMUM_MONEY."""
        return player.money() >= street.hotel_cost() + self.MINIMUM_MONEY
    
    def desire_of_selling_house(self, player: Player, street: Street) -> bool:
        """Retorna un True indicant si no té MINIMUM_MONEY i per tant, vendrà alguna casa si es pot"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_selling_hotel(self, player: Player, street: Street) -> bool:
        """Retorna un True indicant si no té MINIMUM_MONEY i per tant, vendrà algun hotel si es pot"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_mortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un True si després de vendre tot el possible, segueix per sota de MINIMUM_MONEY"""
        return player.money() < self.MINIMUM_MONEY
    
    def desire_of_unmortgaging(self, player: Player, property: Property) -> bool:
        """Retorna un True si ja té prous diners estalviat per deshipotecar propietats"""
        return player.money() >= self.UNMORTGAGE_MONEY
