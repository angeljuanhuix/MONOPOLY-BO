import pytest
from card import build_card, Street
from player import Player
from board import Board
from strategies import Simple_Strategy

# 1. CREEM CLASSES DE SUPORT (Mocks manuals)
class FakeTile:
    """Simula una casella qualsevol per evitar errors de 'NoneType'."""
    def land_on(self, player: Player):
        pass # No cal que faci res per aquests tests

class BoardDeTest(Board):
    """Hereta de Board però anul·la el constructor que carrega JSONs."""
    def __init__(self):
        self._tiles = [FakeTile() for _ in range(40)]
        self._players = []

    def tiles(self):
        return self._tiles

    def players(self):
        return self._players

# 2. FIXTURES AMB LES TEVES CLASSES REALS
@pytest.fixture
def test_board():
    return BoardDeTest()

@pytest.fixture
def p1(test_board):
    # Utilitzem la teva classe Player real
    return Player(test_board, "P1", "Barret", "Groc", 1500, Simple_Strategy())

@pytest.fixture
def p2(test_board):
    return Player(test_board, "P2", "Cotxe", "Roig", 1500, Simple_Strategy())

# 3. EL TEST QUE COBREIX LES 11 CARTES
def test_card_types_coverage(test_board, p1: Player, p2: Player):
    test_board._players = [p1, p2]

    # --- BLOC MOVIMENT ---
    # 1. MoveToPosition (Passant per GO: 30 -> 5 ha de cobrar 200)
    p1.set_position(30)
    build_card({"id": 1, "title": "A", "description": "D", "action": "move_to_position", "position": 5}).execute(p1)
    assert p1.position() == 5
    assert p1.money() == 1700 

    # 2. MoveToNearestStation (De 12 a 15)
    p1.set_position(12)
    build_card({"id": 2, "title": "A", "description": "D", "action": "move_to_nearest_station", "rentMultiplier": 2}).execute(p1)
    assert p1.position() == 15

    # 3. MoveToNearestUtility (De 15 a 28)
    p1.set_position(15)
    build_card({"id": 3, "title": "A", "description": "D", "action": "move_to_nearest_utility", "rentMultiplier": 10}).execute(p1)
    assert p1.position() == 28

    # 4. MoveBackSpaces (10 -> 7)
    p1.set_position(10)
    build_card({"id": 4, "title": "A", "description": "D", "action": "move_back_spaces", "spaces": 3}).execute(p1)
    assert p1.position() == 7

    # --- BLOC ECONOMIA I PRESÓ ---
    # 5. GoToJail
    build_card({"id": 5, "title": "A", "description": "D", "action": "go_to_jail", "position": 10}).execute(p1)
    # Aquí l'assert dependrà de si el teu Player.go_to_prison() canvia un booleà intern

    # 6. GetOutOfJailCard
    build_card({"id": 6, "title": "A", "description": "D", "action": "get_out_of_jail_card", "keepCard": True}).execute(p1)
    assert p1.get_out_of_jail_free_cards() == 1

    # 7. CollectMoney
    build_card({"id": 7, "title": "A", "description": "D", "action": "collect_money", "amount": 100}).execute(p1)
    assert p1.money == 1800

    # 8. PayMoney
    build_card({"id": 8, "title": "A", "description": "D", "action": "pay_money", "amount": 50}).execute(p1)
    assert p1.money() == 1750

    # --- BLOC COMPLEX ---
    # 9. PayPerProperty (1 casa = 25$, 1 hotel = 100$)
    s1 = Street(test_board, 1, "S1", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s1.houses = 1
    s1.hotels = 1
    # Substituïm temporalment la funció perquè retorni el nostre carrer real
    p1.owned_properties = lambda: [s1]
    build_card({"id": 9, "title": "A", "description": "D", "action": "pay_per_property", "amountPerHouse": 25, "amountPerHotel": 100}).execute(p1)
    assert p1.money() == 1625 # 1750 - 125

    # 10. PayEachPlayer
    m1 = p1.money()
    m2 = p2.money()
    build_card({"id": 10, "title": "A", "description": "D", "action": "pay_each_player", "amountPerPlayer": 50}).execute(p1)
    assert p1.money() == m1 - 50
    assert p2.money() == m2 + 50

    # 11. CollectFromPlayers
    m1 = p1.money()
    m2 = p2.money()
    build_card({"id": 11, "title": "A", "description": "D", "action": "collect_from_players", "amountPerPlayer": 20}).execute(p1)
    assert p1.money() == m1 + 20
    assert p2.money() == m2 - 20