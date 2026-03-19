from board import Board
import random



def main() -> None:
    """
    Inicialitza el taulell i la partida 
    i s'escullen la quantitat de jugadors"""

    random.seed(25)

    num_players = int(input("Quants jugadors vols? (2-4) ->"))
    board = Board(
        tiles_json_path="JSON/tiles.json",
        chance_json_path="JSON/chance.json",
        community_chest_json_path="JSON/community-chest.json",
        players_json_path="JSON/players.json",
        num_players = num_players
    )

    board.play()

    
    
    

if __name__ == "__main__":
    main()
