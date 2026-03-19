import pickle
from player import Player, build_player
from tile import Tile, build_tile, Utility, chance, community_chest, special, Street
import json
import random
from const import NUM_TILES
from deck import Deck


class Board:
    """Gestiona el taulell, jugadors, caselles, les baralles i la lògica del joc"""
    def __init__(self, tiles_json_path: str, chance_json_path: str, community_chest_json_path: str, players_json_path: str, num_players: int):
        """Inicialitza el taulell carregant totes les dades des dels fitxers JSON"""

        # Es carreguen les caselles
        with open(tiles_json_path, 'r', encoding = "UTF-8") as file:
            data_tiles = json.load(file)
        self._tiles = [build_tile(self, data_tiles[i]) for i in range(len(data_tiles))]
        
        # Es carreguen els jugadors
        with open(players_json_path, 'r', encoding = "UTF-8") as file:
            data_players = json.load(file)
        
        # L'ínxex és important per identificar cada jugador
        self._players = [build_player(self, data_players[i], i) for i in range(num_players)] 
        
        # Es creen i barregen les baralles
        self._chance_deck = Deck(chance_json_path)
        self._chance_deck.shuffle()

        self._community_chest_deck = Deck(community_chest_json_path)
        self._community_chest_deck.shuffle()

        # S'inicialitza que comenci sempre la mateixa persona (Jordi) i el torn comença actiu
        self._current_player_index = 0
        self._turn_player = True
    
    def chance_deck(self) -> Deck:
        """Retorna el piló de les cartes tipus CHANCE"""
        return self._chance_deck

    def community_chest_deck(self) -> Deck:
        """Retorna el piló de les cartes tipus COMMUNITY_CHEST"""
        return self._community_chest_deck
    
    def players(self) -> list[Player]:
        """Retorna la llista de jugadors de la partida"""
        return self._players

    def tiles(self) -> list[Tile]:
        """Retorna la llista de les caselles del joc"""
        return self._tiles

    def dice(self) -> tuple[int, int]:
        """Retorna els valors actuals dels daus sense tornar-los a llençar"""
        return self._current_dice
    
    def current_dice(self) -> tuple[int, int]: #Mirar el README (1)
        """Llança els daus i retorna els valors obtinguts"""
        self._current_dice = (random.randint(1,6), random.randint(1,6))
        return self._current_dice

    def current_player(self) -> Player: 
        """Retorna el jugador que té el torn actual"""
        return self._players[self._current_player_index]

    def jail_position(self) -> int:
        """Retorna la casella en què es troba la presó"""
        return 10
    
    def number_tiles(self) -> int:
        """Retorna el nombre de caselles del taulell"""
        return 40
    
    def turn_player(self) -> bool:
        """Retorna si un jugador té el torn actiu o no"""
        return self._turn_player
    
    def execute_tile(self, image_frame: int) -> int:
        """Executa l'acció de la casella on cau el jugador actual"""
        from draw import draw
        
        #Obtenim la casella on és el jugador
        current_tile = self._tiles[self.current_player().position()]

        # FRAME EXTRA si és Utility: 
        # 1r Frame: El moviment     2n Frame: Llançament de daus per saber el preu del lloguer
        if isinstance(current_tile, Utility) and not current_tile.availability(): 
            draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
            image_frame += 1
                    
        #FRAME EXTRA per mostrar la casella abans d'executar la carta
        if isinstance(current_tile, (chance, community_chest)):
            draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
            image_frame += 1

        #FRAME EXTRA per mostrar la casella abans de moure's a la presó
        if isinstance(current_tile, (special)) and current_tile.name() == "Go To Jail":
            draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
            image_frame += 1
                    
        
        current_tile.land_on(self.current_player())

        self.check_bankruptcy()

        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg") 
        image_frame += 1

        return image_frame

    def post_movement_actions(self, image_frame: int) -> int:
        """
        Executa les accions post-moviment del jugador actual segons la seva estratègia.
        Ordre d'execució: primer vendre/hipotecar i després construir.
        Cada acció genera un frame nou per mostrar el canvi al taulell.
        Es fan diferents passades per garantir una construcció uniforme"""
        
        from draw import draw
        
        player = self.current_player()
        
        # Múltiples passades fins que no es puguin fer més accions (vendre/hipotecar/deshipotecar)
        action_done = True
        while action_done:
            action_done = False
            for property in player.owned_properties():
                if isinstance(property, Street):
                    #Vendre hotel segons l'estratègia i si es pot fer
                    if player.wants_to_sell_hotel(property) and property.can_sell_hotel():
                        property.sell_hotel()
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True
                    
                    #Vendre casa segons l'estratègia i si es pot fer
                    if player.wants_to_sell_house(property) and property.can_sell_house():
                        property.sell_house()
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True

                #Hipotecar propietat segons l'estratègia i si es pot fer
                if player.wants_to_mortgage(property) and property.can_mortgage():
                    property.do_mortgage()
                    draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                    image_frame += 1
                    action_done = True
                
                #Hipotecar propietat segons l'estratègia i si es pot fer
                if player.wants_to_unmortgage(property) and property.can_unmortgage():
                    property.do_unmortgage()
                    draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                    image_frame += 1
                    action_done = True
        
        # Múltiples passades fins que no es puguin fer més accions (construir)
        action_done = True
        while action_done:
            action_done = False
            for property in player.owned_properties():
                if isinstance(property, Street):
                    #Construir casa segons l'estratègia i si es pot fer
                    if player.wants_to_build_house(property) and property.can_build_house():
                        property.build_house()
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True
                    #Construir hotel segons l'estratègia i si es pot fer
                    if player.wants_to_build_hotel(property) and property.can_build_hotel():
                        property.build_hotel()
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                        action_done = True

        return image_frame
    
    def check_bankruptcy(self) -> None:
        """
        Comprova si algun jugador ha anat a la fallida, i si és el cas,
        executa tot el procés de canvis que succeixen quan se'n va a la fallida
        """

        bankrupt_players = [player for player in self._players if player.broke() and not player.is_bankrupt()]
        
        for player in bankrupt_players:
            print(f"{player.name()} ha fet bancarota!")
            
            # Alliberar propietats (tornen al banc)
            for property in player.owned_properties():
                property.release_property()
            
            # Tornar targetes de sortida de presó al piló corresponent
            for card in player.get_out_of_jail_cards():
                card.deck().return_get_out_of_jail_card(card)
            
            # Buidar targetes i propietats del jugador
            player.clear_jail_cards()
            player.clear_properties()

            # Marcar el jugador
            player.go_bankrupt()

    def play(self) -> None: 
        """Mètode principal. Gestiona tot el que passa durant la partida"""
        from draw import draw

        #GENERACIÓ DE LA IMATGE DEL TAULELL ABANS DE COMENÇAR
        image_frame = 0 
        self._current_dice = (0, 0)
        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
        image_frame += 1

        # Es va executant fins que quedi un jugador o es passing de més de 2000 frames
        while sum(1 for p in self._players if not p.is_bankrupt()) > 1 and image_frame < 2000: 
            
            self._num_double = 0
            
            # Bucle del torn del jugador
            while self._turn_player:
                
                dice1, dice2 = self.current_dice() 
                steps = dice1 + dice2

                # Gestió quan el jugador és a la presó
                if self.current_player().is_in_prison():
                    self.current_player().add_turn_in_prison()

                    # Surt de la presó tirant dobles
                    if dice1 == dice2:
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)


                    # Surt de la presó utilitzant una targeta 
                    elif self.current_player().get_out_of_jail_free_cards() > 0:
                        
                        card = self.current_player().use_get_out_of_jail_card()
                        card.deck().return_get_out_of_jail_card(card)
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)

                    # Surt de la presó quan ja porta tres torns
                    elif self.current_player().turns_in_prison() == 3:
                        self.current_player().leave_prison()
                        self.current_player().move(steps, NUM_TILES)
                        image_frame = self.execute_tile(image_frame)
                    
                    else: # Si hi segueix, es genera frame quan està a la presó
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg")
                        image_frame += 1
                    
                    break # S'acaba el torn de la presó

                else: # Torn normal, el jugador no és a la presó

                    if dice1 == dice2: 
                        print(f"El jugador {self.current_player().name()} ha fet DOBLE en el torn {image_frame}")
                        self._num_double += 1
                        
                    #Tres dobles seguits = Anar a la presó
                    if self._num_double == 3:
                        print(f"El jugador {self.current_player().name()} se'n va a la presó per fer dobles tres cops {image_frame}")
                        self.current_player().go_to_prison() #ENVIAMENT A LA PRESÓ
                        draw(self, f"CODIS/images/i{str(image_frame).zfill(5)}.svg") #Generem la i 
                        image_frame += 1
                        
                        break # S'acaba torn del jugador
                        
                    # Moviment normal i execució de la casella
                    self.current_player().move(steps, NUM_TILES)
                    image_frame = self.execute_tile(image_frame)
                    
                    # El jugador només fa accions post moviments si no ha anat a la fallida abans
                    if not self.current_player().is_bankrupt():
                        image_frame = self.post_movement_actions(image_frame)
                    
                    
                    # El torn acaba si compleix algunes d'aquestes condicions
                    if dice1 != dice2 or self.current_player().is_bankrupt() or self.current_player().is_in_prison():
                        break 
                
            # Canvi de jugador saltant-nos els que estan en fallida
            self._current_player_index = (self._current_player_index + 1) % len(self._players)
            while self.current_player().is_bankrupt():
                self._current_player_index = (self._current_player_index + 1) % len(self._players) 
            
                                                                              

def save_board(board: Board, pickle_path: str) -> None:
    with open(pickle_path, "wb") as f:
        pickle.dump(board, f)


def load_board(pickle_path: str) -> Board:
    with open(pickle_path, "rb") as f:
        return pickle.load(f)
