import pickle
from player import Player, build_player
from tile import Tile, build_tile, Utility, chance, community_chest, special, Street
import json
import random
from const import NUM_TILES
from deck import Deck


class Board:
    def __init__(self, tiles_json_path: str, chance_json_path: str, community_chest_json_path: str, players_json_path: str, num_players: int):
        #ES CARREGA L'INFORMACIÓ DE TOT EL QUE NECESSITEM DEL FITXERS JSON

        with open(tiles_json_path, 'r', encoding = "UTF-8") as file:
            data_tiles = json.load(file)
        self._tiles = [build_tile(self, data_tiles[i]) for i in range(len(data_tiles))]
        
        with open(players_json_path, 'r', encoding = "UTF-8") as file:
            data_players = json.load(file)
            #IMPORTANT, la i del tercer apartat de "build_player" és important, ja que fa referència a l'index de cada jugador
        self._players = [build_player(self, data_players[i], i) for i in range(num_players)] 
        
        self._chance_deck = Deck(chance_json_path)
        self._chance_deck.shuffle()

        self._community_chest_deck = Deck(community_chest_json_path)
        self._community_chest_deck.shuffle()

        #S'INICIALITZA QUE SEMPRE COMENCI LA MATEIXA PERSONA ("Jordi")
        self._current_player_index = 0
        self._turn_player = True
    
    def chance_deck(self) -> Deck:
        """Retorna el piló de les cartes tipus CHANCE"""
        return self._chance_deck

    def community_chest_deck(self) -> Deck:
        """Retorna el piló de les cartes tipus COMMUNITY_CHEST"""
        return self._community_chest_deck
    
    def players(self) -> list[Player]:
        """Retorna la llista de jugadors"""
        return self._players

    def tiles(self) -> list[Tile]:
        """Retorna la llista de caselles"""
        return self._tiles

    def dice(self) -> tuple[int, int]:
        """Retorna els valors actuals dels daus"""
        return self._current_dice
    
    def current_dice(self) -> tuple[int, int]: #Mirar el README (1)
        """Retorna els valors actuals dels daus"""
        self._current_dice = (random.randint(1,6), random.randint(1,6))
        return self._current_dice

    def current_player(self) -> Player: 
        """Retorna el jugador actual"""
        return self._players[self._current_player_index]

    def jail_position(self) -> int:
        """Retorna la casella en què es troba la presó"""
        return 10
    
    def number_tiles(self) -> int:
        """Retorna el nombre de caselles del taulell"""
        return 40
    
    def turn_player(self) -> bool:
        """Retorna si un jugador ha fet el seu torn o no"""
        return self._turn_player
    
    def execute_tile(self, image_frame: int) -> int:

        from draw import draw
        #Assignem la casella on cau
        current_tile = self._tiles[self.current_player().position()]

        # Frame extra si és Utility perquè s'ha de pagar lloguer, ja que tirarà dues vegades, la primera per moure's i la segona per saber quant ha de pagar
        if isinstance(current_tile, Utility) and not current_tile.availability(): 
            draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
            image_frame += 1
                    
        #Frame extra per mostrar l'execució de la carta
        if isinstance(current_tile, (chance, community_chest)):
            draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
            image_frame += 1

        #Frame extra per quan cau en el Go To Jail
        if isinstance(current_tile, (special)) and current_tile.name() == "Go To Jail":
            draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
            image_frame += 1
                    
        
        current_tile.land_on(self.current_player())

        self.check_bankruptcy()

        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg") 
        image_frame += 1

        return image_frame

    def post_movement_actions(self, image_frame: int) -> int:

        from draw import draw
        
        player = self.current_player()
        
        # Vendre i hipotecar amb múltiples passades
        action_done = True
        while action_done:
            action_done = False
            for property in player.owned_properties():
                if isinstance(property, Street):
                    if player.wants_to_sell_hotel(property) and property.can_sell_hotel():
                        property.sell_hotel()
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True
                    if player.wants_to_sell_house(property) and property.can_sell_house():
                        property.sell_house()
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True
                if player.wants_to_mortgage(property) and property.can_mortgage():
                    property.do_mortgage()
                    draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                    image_frame += 1
                    action_done = True
                if player.wants_to_unmortgage(property) and property.can_unmortgage():
                    property.do_unmortgage()
                    draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                    image_frame += 1
                    action_done = True
        
        # Construir amb múltiples passades
        action_done = True
        while action_done:
            action_done = False
            for property in player.owned_properties():
                if isinstance(property, Street):
                    if player.wants_to_build_house(property) and property.can_build_house():
                        property.build_house()
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True
                    if player.wants_to_build_hotel(property) and property.can_build_hotel():
                        property.build_hotel()
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True

        return image_frame
    
    def check_bankruptcy(self) -> None:
        bankrupt_players = [player for player in self._players if player.broke() and not player.is_bankrupt()]
        
        for player in bankrupt_players:
            print(f"{player.name()} ha fet bancarota!")
            
            # Alliberar propietats
            for property in player.owned_properties():
                property.release_property()
            
            # Tornar targetes de sortida de presó al piló
            for card in player.get_out_of_jail_cards():
                card.deck().return_get_out_of_jail_card(card)
            
            player.clear_jail_cards()
            player.clear_properties()
            player.go_bankrupt()
    def play(self) -> None: 
        """
        Permet jugar al monopoly i és on hi ha tot el codi important
        com els moviments, si hi ha dobles o no...
        """
        from draw import draw

        #GENERACIÓ DE LA IMATGE DEL TAULELL ABANS DE COMENÇAR
        
        image_frame = 0 #El nombre de la imatge en cada moment
        
        self._current_dice = (0, 0)
        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
        
        image_frame += 1

        while sum(1 for p in self._players if not p.is_bankrupt()) > 1 and image_frame < 600: 
            
            self._num_double = 0
            
            #Bucle que s'anirà executant fins que passi el torn del jugador
            while self._turn_player:
                
                dice1, dice2 = self.current_dice() #Assignem valors a les dues tirades de daus
                steps = dice1 + dice2

                if self.current_player().is_in_prison():
                    self.current_player().add_turn_in_prison()

                    if dice1 == dice2:
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)

                    elif self.current_player().get_out_of_jail_free_cards() > 0:
                        
                        card = self.current_player().use_get_out_of_jail_card()
                        card.deck().return_get_out_of_jail_card(card)
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)

                    elif self.current_player().turns_in_prison() == 3:
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)
                    
                    else:
                        
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                    
                    break

                else: # Si no hi és, doncs tot normal

                    #Comprovem si és un doble
                    if dice1 == dice2: 
                        print(f"El jugador {self.current_player().name()} ha fet DOBLE en el torn {image_frame}")
                        self._num_double += 1
                        
                    #Tres dobles seguits = Anar a presó
                    if self._num_double == 3:
                        print(f"El jugador {self.current_player().name()} se'n va a la presó per fer dobles tres cops {image_frame}")
                        self.current_player().go_to_prison() #ENVIAMENT A LA PRESÓ
                        draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg") #Generem la imatge 
                        image_frame += 1
                        
                        break #Parem el bucle perquè s'ha acabat el torn del jugador
                        
                    #TORN NORMAL. Si s'arriba aquí, significa que no ha arribat a 3 dobles o directament no n'ha fet cap
                    self.current_player().move(steps, NUM_TILES)

                    #S'executa tot el necessari
                    image_frame = self.execute_tile(image_frame)
                    
                    if not self.current_player().is_bankrupt():
                        image_frame = self.post_movement_actions(image_frame)
                    
                    
                    #CONDICIÓ PER A QUÈ S'ACABI EL BUCLE DEL TORN
                    if dice1 != dice2 or self.current_player().is_bankrupt() or self.current_player().is_in_prison():
                        break #Parem bucle, ja que no és doble i s'ha acabat el seu torn
                
            #Fem que l'index del jugador vagi canviant i com és una llista, ens interessa que quan arribi al 4 torni a
            #la posició 0 perquè al final, es comporta com una llista, que va del 0 al 3

            self._current_player_index = (self._current_player_index + 1) % len(self._players)
            while self.current_player().is_bankrupt():
                self._current_player_index = (self._current_player_index + 1) % len(self._players) 
            
                                                                              

def save_board(board: Board, pickle_path: str) -> None:
    with open(pickle_path, "wb") as f:
        pickle.dump(board, f)


def load_board(pickle_path: str) -> Board:
    with open(pickle_path, "rb") as f:
        return pickle.load(f)
