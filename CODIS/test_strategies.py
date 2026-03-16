from player import Player
from board import Board
from strategies import Simple_Strategy, Smart_Strategy
from tile import Street
from typing import cast


def test_player_simple_strategy_desire_buying() -> None:
    """Comprova que la Simple_Strategy decideix bé en funció dels diners."""

    mock_board = cast(Board, None)

    player = Player(board=mock_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Simple_Strategy())
    
    # 1. Volem que tingui 1000$. Com que comença amb START_MONEY (750), n'hi sumem 250.
    player.pay(player.money())
    player.receive(1000)
    
    carrer = Street(mock_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    # 2. Amb 1000$, hauria de voler comprar un carrer de 200$
    assert player.wants_to_buy(carrer) is True
    
    # 3. Ara l'arruïnem: volem que li quedin només 50$. 
    # Com que en té 1000, li fem pagar 950$.
    player.pay(950)
    
    # 4. Amb 50$, NO hauria de voler (ni poder) comprar un carrer de 200$
    assert player.wants_to_buy(carrer) is False

def test_player_simple_strategy_other_desires() -> None:
    """Comprova que els altres desires donen False independentment dels diners que té."""

    mock_board = cast(Board, None)

    player = Player(board=mock_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Simple_Strategy())
    
    # 1. Volem que tingui 1000$. Com que comença amb START_MONEY (750), n'hi sumem 250.
    player.pay(player.money())
    player.receive(1000)
    
    carrer = Street(mock_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    #Dona igual quants diners tingui, que ha de donar sempre False
    assert player.wants_to_build_house(carrer) is False
    assert player.wants_to_build_hotel(carrer) is False
    assert player.wants_to_sell_house(carrer) is False
    assert player.wants_to_sell_hotel(carrer) is False
    assert player.wants_to_mortgage(carrer) is False
    assert player.wants_to_unmortgage(carrer) is False

def test_player_smart_strategy_rich() -> None:
    """Comprova que la Smart_Strategy decideix construir, vendre o hipotecar segons els diners."""
    mock_board = cast(Board, None)
    
    # ATENCIÓ: Ara sí que li passem la Smart_Strategy!
    player = Player(board=mock_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(mock_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    
    player.pay(player.money()) # Buidem cartera
    player.receive(1000)
    
    assert player.wants_to_buy(carrer) is True
    assert player.wants_to_build_house(carrer) is True   # 1000 >= 200 + 150
    assert player.wants_to_build_hotel(carrer) is True   # 1000 >= 200 + 150
    assert player.wants_to_sell_house(carrer) is False   # 1000 no és < 150
    assert player.wants_to_sell_hotel(carrer) is False   # 1000 no és < 150
    assert player.wants_to_mortgage(carrer) is False     # 1000 no és < 150
    assert player.wants_to_unmortgage(carrer) is True    # 1000 >= 300

def test_player_smart_strategy_regular() -> None:
    """Comprova que la Smart_Strategy decideix construir, vendre o hipotecar segons els diners."""
    mock_board = cast(Board, None)
    
    # ATENCIÓ: Ara sí que li passem la Smart_Strategy!
    player = Player(board=mock_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(mock_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    # --- ESCENARI 2: ESTABLE (200$) ---
    # Pot pagar una casa (200) però no li quedaria el marge de 150. Tampoc està per sota de 150.
    player.pay(player.money())
    player.receive(200)
    
    assert player.wants_to_buy(carrer) is False
    assert player.wants_to_build_house(carrer) is False  # 200 no és >= 350
    assert player.wants_to_build_hotel(carrer) is False  # 200 no és >= 350
    assert player.wants_to_sell_house(carrer) is False   # 200 no és < 150
    assert player.wants_to_sell_hotel(carrer) is False   # 200 no és < 150
    assert player.wants_to_mortgage(carrer) is False     # 200 no és < 150
    assert player.wants_to_unmortgage(carrer) is False   # 200 no és >= 300
    
def test_player_smart_strategy_poor() -> None:
    """Comprova que la Smart_Strategy decideix construir, vendre o hipotecar segons els diners."""
    mock_board = cast(Board, None)
    
    # ATENCIÓ: Ara sí que li passem la Smart_Strategy!
    player = Player(board=mock_board, name="Test", piece="Hat", color="Blue", index=0, strategy=Smart_Strategy())
    
    # Cost casa/hotel = 200
    carrer = Street(mock_board, 37, "Park Lane", "property", "dark_blue", 350, 35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175 
    )
    # --- ESCENARI 3: POBRE / DESESPERAT (100$) ---
    player.pay(player.money())
    player.receive(100)
    
    assert player.wants_to_buy(carrer) is False
    assert player.wants_to_build_house(carrer) is False  # No té diners
    assert player.wants_to_build_hotel(carrer) is False  # No té diners
    assert player.wants_to_sell_house(carrer) is True    # 100 < 150 (Pànic, venem!)
    assert player.wants_to_sell_hotel(carrer) is True    # 100 < 150 (Pànic, venem!)
    assert player.wants_to_mortgage(carrer) is True      # 100 < 150 (Pànic, hipotequem!)
    assert player.wants_to_unmortgage(carrer) is False   # 100 no és >= 300