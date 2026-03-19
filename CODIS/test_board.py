import pytest
import os
from board import Board
from tile import Property

@pytest.fixture
def test_board() -> Board:
    base_path = os.path.dirname(os.path.abspath(__file__))
    return Board(
        tiles_json_path=os.path.join(base_path, "../JSON/tiles.json"),
        chance_json_path=os.path.join(base_path, "../JSON/chance.json"),
        community_chest_json_path=os.path.join(base_path, "../JSON/community-chest.json"),
        players_json_path=os.path.join(base_path, "../JSON/players.json"),
        num_players=3
    )


def test_number_tiles(test_board: Board) -> None:
    """Comprova que el nombre de caselles és 40"""
    assert test_board.number_tiles() == 40

def test_players_count(test_board: Board) -> None:
    """Comprova que el tauler té el nombre correcte de jugadors"""
    assert len(test_board.players()) == 3

def test_jail_position(test_board: Board) -> None:
    """Comprova que la posició de la presó és 10"""
    assert test_board.jail_position() == 10

def test_current_player_is_first(test_board: Board) -> None:
    """Comprova que el jugador actual és el primer"""
    assert test_board.current_player() == test_board.players()[0]

def test_current_dice_range(test_board: Board) -> None:
    """Comprova que els daus retornen valors entre 1 i 6"""
    dice1, dice2 = test_board.current_dice()
    assert 1 <= dice1 <= 6
    assert 1 <= dice2 <= 6

# FUNCIÓ CHECK BANKRUPTCY

def test_check_bankruptcy_marks_player(test_board: Board) -> None:
    """Comprova que un jugador amb diners negatius fa fallida"""
    player = test_board.players()[0]
    player.pay(2500) #Ens assegurem que estigui en nombres negatius
    test_board.check_bankruptcy()
    assert player.is_bankrupt()

def test_check_bankruptcy_resets_money(test_board: Board) -> None:
    """Comprova que els diners es posen a 0 en fallida"""
    player = test_board.players()[0]
    player.pay(2500) #Ens assegurem que estigui en nombres negatius
    test_board.check_bankruptcy()
    assert player.money() == 0

def test_check_bankruptcy_releases_properties(test_board: Board) -> None:
    """Comprova que les propietats s'alliberen quan s'està en fallida"""
    player = test_board.players()[0]
    street = test_board.tiles()[1]
    assert isinstance(street, Property)  # Pylance ja sap que és Property
    street.buy(player)
    player.pay(2500) #Ens assegurem que estigui en fallida
    test_board.check_bankruptcy()
    assert street.owner is None

def test_check_bankruptcy_clears_properties(test_board: Board) -> None:
    """Comprova que la llista de propietats del jugador es buida"""
    player = test_board.players()[0]
    street = test_board.tiles()[1]
    assert isinstance(street, Property)  # Pylance ja sap que és Property
    street.buy(player)
    player.pay(2500) #Ens assegurem que estigui en fallida
    test_board.check_bankruptcy()
    assert len(player.owned_properties()) == 0

def test_check_bankruptcy_only_affects_broke_players(test_board: Board) -> None:
    """Comprova que només afecta jugadors amb diners negatius"""
    player1 = test_board.players()[0]
    player2 = test_board.players()[1]
    player1.pay(2500) #Ens assegurem que estigui en nombres negatius
    test_board.check_bankruptcy()
    assert player1.is_bankrupt()
    assert not player2.is_bankrupt()

def test_check_bankruptcy_not_broke_positive_money(test_board: Board) -> None:
    """Comprova que no se'n va a la fallida si té diners positius"""
    player = test_board.players()[0]
    test_board.check_bankruptcy()
    assert not player.is_bankrupt()