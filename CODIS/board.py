import pickle
from player import Player, build_player
from tile import Tile, build_tile
import json
import random
from const import NUM_TILES


class Board:
    def __init__(self, tiles_json_path: str, chance_json_path: str, community_chest_json_path: str, players_json_path: str):
        """
        self._tiles: list[Any] = []
        
        with open(tiles_json_path, 'r', encoding='UTF-8') as file:
            tiles_data = json.load(file) 

        
        for data in tiles_data:
            casella_nova = build_tile(board?, data)
            self._tiles.append(casella_nova)
        """
        #ES CARREGA L'INFORMACIÓ DE TOT EL QUE NECESSITEM DEL FITXERS JSON

        with open(tiles_json_path, 'r', encoding = "UTF-8") as file:
            data_tiles = json.load(file)
        self._tiles = [build_tile(self, data_tiles[i]) for i in range(len(data_tiles))]
        
        with open(players_json_path, 'r', encoding = "UTF-8") as file:
            data_players = json.load(file)
            #IMPORTANT, la i del tercer apartat de "build_player" és important, ja que fa referència a l'index de cada jugador
        self._players = [build_player(self, data_players[i], i) for i in range(len(data_players))] 
        """
        with open(chance_json_path, 'r', encoding = "UTF-8") as file:
            data_chance = json.load(file)
        self._chance = [build_tile(self, data_chance[i]) for i in range(len(data_chance))]

        with open(community_chest_json_path, 'r', encoding = "UTF-8") as file:
            data_community = json.load(file)
        self._community_chest = [build_tile(self, data_community[i]) for i in range(len(data_community))]
        """

        #S'INICIALITZA QUE SEMPRE COMENCI LA MATEIXA PERSONA ("Jordi")
        self._current_player_index = 0
        self._turn_player = True
    
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

        for _ in range(100): # Quan ho tingui més avançat, aquí posar que de range vagi fins quan quedi una persona FER UN WHILE persones_vives > 1
            
            self._num_double = 0
            
            #Bucle que s'anirà executant fins que passi el torn del jugador
            while self._turn_player:
                
                dice1, dice2 = self.current_dice() #Assignem valors a les dues tirades de daus
                
            
                #Comprovem si és un doble
                if dice1 == dice2: 
                    print(f"El jugador {self.current_player().name()} ha fet DOBLE en el torn {image_frame}")
                    self._num_double += 1
                    
                #Tres dobles seguits = Anar a presó
                if self._num_double == 3:
                    print(f"El jugador {self.current_player().name()} se'n va a la presó per fer dobles tres cops {image_frame}")
                    self.current_player().set_position(self.jail_position()) #ENVIAMENT A LA PRESÓ
                    draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg") #Generem la imatge 
                    image_frame += 1
                    
                    break #Parem el bucle perquè s'ha acabat el torn del jugador
                    
                #TORN NORMAL. Si s'arriba aquí, significa que no ha arribat a 3 dobles o directament no n'ha fet cap
                steps = dice1 + dice2
                self.current_player().move(steps, NUM_TILES)

                #S'executa tot allò relacionat amb la casella en la que ha caigut
                current_tile = self._tiles[self.current_player().position()]
                current_tile.land_on(self.current_player())
                
                draw(self, f"CODIS/images/imatge{str(image_frame).zfill(5)}.svg") 
                image_frame += 1
                
                #CONDICIÓ PER A QUÈ S'ACABI EL BUCLE DEL TORN
                if dice1 != dice2:
                    break #Parem bucle, ja que no és doble i s'ha acabat el seu torn
                
            #Fem que l'index del jugador vagi canviant i com és una llista, ens interessa que quan arribi al 4 torni a
            #la posició 0 perquè al final, es comporta com una llista, que va del 0 al 3

            self._current_player_index = (self._current_player_index + 1) % 4 
            
                                                                              

def save_board(board: Board, pickle_path: str) -> None:
    with open(pickle_path, "wb") as f:
        pickle.dump(board, f)


def load_board(pickle_path: str) -> Board:
    with open(pickle_path, "rb") as f:
        return pickle.load(f)
