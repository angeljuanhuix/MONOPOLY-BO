import pytest
from card import build_card, Street
from player import Player
from board import Board
import os

@pytest.fixture
def test_board() -> Board:
    """Retorna un board real creat per fer testos"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return Board(
        tiles_json_path= os.path.join(base_path, "../JSON/tiles.json"),
        chance_json_path= os.path.join(base_path, "../JSON/chance.json"),
        community_chest_json_path= os.path.join(base_path, "../JSON/community-chest.json"),
        players_json_path=os.path.join(base_path, "../JSON/players.json"),
        num_players=3
    )

@pytest.fixture
def p1(test_board: Board):
    """Retorna un jugador real"""
    players: list[Player] = test_board.players()
    return players[0]

@pytest.fixture
def p2(test_board: Board):
    """Retorna un jugador real"""
    players: list[Player] = test_board.players()
    return players[1]

@pytest.fixture
def p3(test_board: Board):
    """Retorna un jugador real"""
    players: list[Player] = test_board.players()
    return players[2]

# MOVIMENT 

def test_move_to_position_passes_go( p1: Player) -> None:
    """
    Comprova que el jugador rep els diners (si passa pel GO) 
    quan rep una carta de moure's a x posició
    """
    p1.set_position(30)
    build_card({"id": 1, "title": "A", "description": "D", "action": "move_to_position", "position": 5}).execute(p1)
    assert p1.position() == 5
    assert p1.money() == 850 # Comença amb 750$ + 50$ per passar pel GO, però -200$ perquè la posició 5 hi ha una estació
    #i com en aquest test, no té propietari, doncs el jugador la compra. SI ES CANVIEN LES CONSTANTS, AQUEST SORTIRÀ MALAMENT

def test_move_to_nearest_station_from_36(p1: Player) -> None:
    """
    Comprova que el jugador es mogui a l'estació adequada si és 
    entre la posició (35,5). També comprovar que cobra quan passa pel GO
    """
    p1.set_position(36)
    money_before = p1.money()
    build_card({"id": 2, "title": "A", "description": "D", "action": "move_to_nearest_station", "rentMultiplier": 2}).execute(p1)
    assert p1.position() == 5
    assert p1.money() == money_before + 50 - 200  # GO (+50) buy_station(-200)

def test_move_to_nearest_station_from_7(p1: Player) -> None:
    """
    Comprova que el jugador es mogui a l'estació 
    adequada si és entre la posició (5,15). 
    """
    p1.set_position(7)
    build_card({"id": 2, "title": "A", "description": "D", "action": "move_to_nearest_station", "rentMultiplier": 2}).execute(p1)
    assert p1.position() == 15

def test_move_to_nearest_station_from_22(p1: Player) -> None:
    """
    Comprova que el jugador es mogui a l'estació 
    adequada si és entre la posició (15,25). 
    """
    p1.set_position(22)
    build_card({"id": 2, "title": "A", "description": "D", "action": "move_to_nearest_station", "rentMultiplier": 2}).execute(p1)
    assert p1.position() == 25

def test_move_to_nearest_station_from_28(p1: Player) -> None:
    """
    Comprova que el jugador es mogui a l'estació 
    adequada si és entre la posició (25,35). 
    """
    p1.set_position(28)
    build_card({"id": 2, "title": "A", "description": "D", "action": "move_to_nearest_station", "rentMultiplier": 2}).execute(p1)
    assert p1.position() == 35

def test_move_to_nearest_utility(p1: Player) -> None:
    """
    Comprova que el jugador es mogui a la Utility
    adequada si és entre la posició (12,28). 
    """
    p1.set_position(15)
    build_card({"id": 3, "title": "A", "description": "D", "action": "move_to_nearest_utility", "rentMultiplier": 10}).execute(p1)
    assert p1.position() == 28

def test_move_back_spaces(p1: Player) -> None:
    """Comprova que es mogui 3 posicions endarrere correctament"""
    p1.set_position(7)
    build_card({"id": 4, "title": "A", "description": "D", "action": "move_back_spaces", "spaces": 3}).execute(p1)
    assert p1.position() == 4

# PRESÓ

def test_go_to_jail(p1: Player) -> None:
    """
    Comprova que si el jugador li toca aquesta carta,
    va a la presó i el seu estat i posició és la correcte
    """
    build_card({"id": 5, "title": "A", "description": "D", "action": "go_to_jail", "position": 10}).execute(p1)
    assert p1.is_in_prison() == True
    assert p1.position() == 10

def test_get_out_of_jail_card(p1: Player) -> None:
    build_card({"id": 6, "title": "A", "description": "D", "action": "get_out_of_jail_card", "keepCard": True}).execute(p1)
    assert p1.get_out_of_jail_free_cards() == 1

# DINERS
def test_collect_money(p1: Player) -> None:
    """Comprova que el jugador rep els diners indicats per la carta"""
    money_before = p1.money()
    build_card({"id": 7, "title": "A", "description": "D", "action": "collect_money", "amount": 100}).execute(p1)
    assert p1.money() == money_before + 100

def test_pay_money(p1: Player) -> None:
    """Comprova que el jugador paga els diners indicats per la carta"""
    money_before = p1.money()
    build_card({"id": 8, "title": "A", "description": "D", "action": "pay_money", "amount": 50}).execute(p1)
    assert p1.money() == money_before - 50

# MÉS GENERALS

def test_pay_per_property(test_board: Board, p1: Player) -> None:
    """Comprova que el jugador paga els diners que li toquen per casa"""
    s1 = Street(test_board, 1, "S1", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s2 = Street(test_board, 3, "S2", "property", "brown", 60, 4, 8, 20, 60, 180, 320, 450, 50, 50, 30)
    s1.buy(p1)
    s2.buy(p1)
    for _ in range(4):
        s1.build_house()
        s2.build_house()
    money_before = p1.money()
    build_card({"id": 9, "title": "A", "description": "D", "action": "pay_per_property", "amountPerHouse": 25, "amountPerHotel": 100}).execute(p1)
    assert p1.money() == money_before - 200  # 8 cases * 25$

def test_pay_each_player(p1: Player, p2: Player, p3: Player) -> None:
    """
    Comprova altres jugadors reben la quantitat que indica la 
    carta i el jugador que l'ha executat, ha pagat el que li toca
    """
    m1, m2, m3 = p1.money(), p2.money(), p3.money()
    build_card({"id": 10, "title": "A", "description": "D", "action": "pay_each_player", "amountPerPlayer": 50}).execute(p1)
    assert p1.money() == m1 - 100 # paga a cada jugador 50
    assert p2.money() == m2 + 50
    assert p3.money() == m3 + 50

def test_collect_from_players(p1: Player, p2: Player, p3: Player) -> None:
    """
    Comprova altres jugadors paguen la quantitat que indica la 
    carta i el jugador que l'ha executat, ha rebut el que li toca
    """
    m1, m2, m3 = p1.money(), p2.money(), p3.money()
    build_card({"id": 11, "title": "A", "description": "D", "action": "collect_from_players", "amountPerPlayer": 50}).execute(p1)
    assert p1.money() == m1 + 100  # rep de p2 i p3
    assert p2.money() == m2 - 50
    assert p3.money() == m3 - 50
    