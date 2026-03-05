from board import Board
import random

def main() -> None:
    board = Board(
        tiles_json_path="JSON/tiles.json",
        chance_json_path="JSON/chance.json",
        community_chest_json_path="JSON/community-chest.json",
        players_json_path="JSON/players.json",
    )

    random.seed(25)
    board.play()

    
    
    

if __name__ == "__main__":
    main()
