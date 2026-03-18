from player import Player
from board import Board
from strategies import Simple_Strategy, Smart_Strategy
from tile import Street
from typing import cast


def test_player_simple_strategy_desire_buying() -> None:
    """
    Comprova que la Simple_Strategy decideix bé en 
    funció dels diners que té el jugador.
    """

    test_board = cast(Board, None)

    player = Player(board=test_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Simple_Strategy())
    
    # Fem que el jugador tingui 1000$ inicialment(li restem el que té i li sumem 1000$)
    player.pay(player.money())
    player.receive(1000)
    
    carrer = Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    #Es comprova que vulgui comprar un carrer de 350$
    assert player.wants_to_buy(carrer) is True
    
    # Es fa arruinar-lo (només li queden 50$)
    player.pay(950)
    
    # Es comprova que no vulgui comprar un carrer de 350$
    assert player.wants_to_buy(carrer) is False

def test_player_simple_strategy_other_desires() -> None:
    """Comprova que els altres desires donen False independentment dels diners que té."""

    test_board = cast(Board, None)

    player = Player(board=test_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Simple_Strategy())
    
    # Comença amb 1000$
    player.pay(player.money())
    player.receive(1000)
    
    carrer = Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    #Independentments dels diners, ha de donar False, perquè així és l'estratègia
    assert player.wants_to_build_house(carrer) is False
    assert player.wants_to_build_hotel(carrer) is False
    assert player.wants_to_sell_house(carrer) is False
    assert player.wants_to_sell_hotel(carrer) is False
    assert player.wants_to_mortgage(carrer) is False
    assert player.wants_to_unmortgage(carrer) is False

def test_player_smart_strategy_rich() -> None:
    """
    Comprova que la Smart_Strategy decideix correctament quan 
    construir, vendre o hipotecar quan té diners
    """
    test_board = cast(Board, None)
    
    player = Player(board=test_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    #S'assigna que tingui 1000$
    player.pay(player.money()) 
    player.receive(1000)
    
    assert player.wants_to_buy(carrer) is True
    assert player.wants_to_build_house(carrer) is True   # 1000 >= 200 + 150
    assert player.wants_to_build_hotel(carrer) is True   # 1000 >= 200 + 150
    assert player.wants_to_sell_house(carrer) is False   # 1000 < 150 (No passa)
    assert player.wants_to_sell_hotel(carrer) is False   # 1000 < 150 (No passa)
    assert player.wants_to_mortgage(carrer) is False     # 1000 < 150 (No passa)
    assert player.wants_to_unmortgage(carrer) is True    # 1000 >= 300

def test_player_smart_strategy_regular() -> None:
    """
    Comprova que la Smart_Strategy decideix correctament quan 
    construir, vendre o hipotecar quan té un capital regular
    """
    test_board = cast(Board, None)
    
    player = Player(board=test_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    # S'assigna que tingui 200$
    player.pay(player.money())
    player.receive(200)
    
    assert player.wants_to_buy(carrer) is False
    assert player.wants_to_build_house(carrer) is False  # 200 >= 350 (No passa)
    assert player.wants_to_build_hotel(carrer) is False  # 200 >= 350 (No passa)
    assert player.wants_to_sell_house(carrer) is False   # 200 < 150 (No passa)
    assert player.wants_to_sell_hotel(carrer) is False   # 200 < 150 (No passa)
    assert player.wants_to_mortgage(carrer) is False     # 200 < 150 (No passa)
    assert player.wants_to_unmortgage(carrer) is False   # 200 >= 300 (No passa)
    
def test_player_smart_strategy_poor() -> None:
    """
    Comprova que la Smart_Strategy decideix correctament quan 
    construir, vendre o hipotecar quan és pobre
    """
    test_board = cast(Board, None)
    
    player = Player(board=test_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    # S'assigna que tingui 200$
    player.pay(player.money())
    player.receive(100)
    
    assert player.wants_to_buy(carrer) is False
    assert player.wants_to_build_house(carrer) is False  # No té diners
    assert player.wants_to_build_hotel(carrer) is False  # No té diners
    assert player.wants_to_sell_house(carrer) is True    # 100 < 150 (Es ven)
    assert player.wants_to_sell_hotel(carrer) is True    # 100 < 150 (Es ven)
    assert player.wants_to_mortgage(carrer) is True      # 100 < 150 (Es ven)
    assert player.wants_to_unmortgage(carrer) is False   # 100 >= 300 (No té prous diners)