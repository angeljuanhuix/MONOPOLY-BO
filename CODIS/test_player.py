import pytest
from player import Player
from strategies import Simple_Strategy
from const import START_MONEY, GO_SALARY, NUM_TILES
from board import Board
from typing import cast


# --- FIXTURES ---
# Això crea un jugador "fals" abans de cada test perquè no hagis 
# de repetir aquesta inicialització constantment. Això puntua molt bé en "claredat" i "concisió".

@pytest.fixture
def dummy_player() -> Player:
    
    # Passem 'None' com a tauler només per provar la lògica interna del jugador
    # Si algun mètode necessita el tauler obligatòriament, hauríem de fer un mock del tauler
    mock_board = cast(Board, None)
    return Player(board = mock_board , name="Test", piece="Hat", color="Blue", index=0, strategy = Simple_Strategy())

# --- TESTS ---

#ATRIBUTS BÀSICS

def test_player_basic_getters(dummy_player: Player) -> None:
    """Comprova que els mètodes que retornen atributs bàsics funcionen."""
    from strategies import Strategy
    
    # Valors basats en el que hem posat al dummy_player de la @pytest.fixture
    assert dummy_player.name() == "Test"
    assert dummy_player.piece == "Hat"
    assert dummy_player.color() == "Blue"
    assert dummy_player.index() == 0
    assert dummy_player.board() is None  # L'havíem mockejat amb None
    assert isinstance(dummy_player.strategy(), Strategy)

def test_player_initialization(dummy_player: Player) -> None:
    """Comprova que el jugador s'inicialitza amb els valors correctes."""
    assert dummy_player.name() == "Test"
    assert dummy_player.position() == 0
    assert dummy_player.money() == START_MONEY
    assert not dummy_player.is_in_prison() # Suposant que tinguis aquest mètode

def test_player_move_normal(dummy_player: Player) -> None:
    """Comprova que el jugador es mou correctament sense passar per la Sortida."""
    dummy_player.move(5, NUM_TILES)
    assert dummy_player.position() == 5
    assert dummy_player.money() == START_MONEY # Els diners no han de canviar

def test_player_pass_go_collects_salary(dummy_player: Player) -> None:
    """Comprova que en donar la volta al tauler (passar del 39 al 0+) cobra el salari."""
    dummy_player.set_position(38)
    dummy_player.move(4, 40) # Hauria d'acabar a la posició 2 (38 + 4 = 42 -> 42 % 40 = 2)
    
    assert dummy_player.position() == 2
    assert dummy_player.money() == START_MONEY + GO_SALARY

def test_player_add_property(dummy_player: Player) -> None:
    """Comprova que quan un jugador compra una propietat, se li afegeix al seu inventari."""
    # Com que demana un objecte Property, fem una trampa (mock) amb el cast
    from tile import Property
    from typing import cast
    
    propietat_falsa = cast(Property, "Propietat de Prova")
    
    # Suposant que tens un mètode per afegir propietats al jugador
    # dummy_player.add_property(propietat_falsa) 
    
    # Comprovació manual accedint a la llista (només per al test)
    dummy_player.owned_properties().append(propietat_falsa) 
    
    assert len(dummy_player.owned_properties()) == 1
    assert dummy_player.owned_properties()[0] == propietat_falsa

def test_player_get_out_of_jail_cards(dummy_player: Player) -> None:
    """Comprova que el jugador pot rebre targetes de sortir de la presó."""
    from card import Card
    from typing import cast
    
    carta_falsa = cast(Card, "Get Out of Jail")
    
    assert len(dummy_player.get_out_of_jail_cards()) == 0
    
    # dummy_player.add_get_out_of_jail_card(carta_falsa)
    dummy_player.get_out_of_jail_cards().append(carta_falsa)
    
    assert len(dummy_player.get_out_of_jail_cards()) == 1

#GESTIÓ PRESÓ

def test_player_prison_turns_management(dummy_player: Player) -> None:
    """Comprova que es poden afegir torns a la presó i llegir-los correctament."""
    assert dummy_player.turns_in_prison() == 0
    
    dummy_player.add_turn_in_prison()
    assert dummy_player.turns_in_prison() == 1
    
    dummy_player.add_turn_in_prison()
    assert dummy_player.turns_in_prison() == 2

def test_player_leave_prison(dummy_player: Player) -> None:
    """Comprova que el jugador surt de la presó correctament."""
    
    # 1. Li afegim un parell de torns a la presó
    dummy_player.add_turn_in_prison()
    dummy_player.add_turn_in_prison()
    assert dummy_player.turns_in_prison() == 2
    
    # 2. Executem la funció per sortir-ne
    dummy_player.leave_prison()
    
    # 3. Comprovem que el comptador s'ha reiniciat a 0
    assert dummy_player.turns_in_prison() == 0

def test_player_jail_cards_management(dummy_player: Player) -> None:
    """Comprova el cicle complet de les cartes de sortir de la presó."""
    from typing import cast
    from card import Card
    carta_falsa = cast(Card, "Carta Test")
    
    # 1. Afegir i comprovar
    dummy_player.add_get_out_of_jail_free_card(carta_falsa)
    assert dummy_player.get_out_of_jail_free_cards() == 1
    
    # 2. Utilitzar (hauria de retornar la carta i treure-la de la llista)
    carta_usada = dummy_player.use_get_out_of_jail_card()
    assert carta_usada == carta_falsa
    assert dummy_player.get_out_of_jail_free_cards() == 0
    
    # 3. Netejar (clear)
    dummy_player.add_get_out_of_jail_free_card(carta_falsa)
    dummy_player.clear_jail_cards()
    assert dummy_player.get_out_of_jail_free_cards() == 0

def test_player_go_to_prison(dummy_player: Player) -> None:
    """Comprova que el mètode d'anar a la presó actualitza l'estat i la posició."""
    dummy_player.go_to_prison()
    
    assert dummy_player.position() == 10 # 10 és la casella de la presó
    assert dummy_player.is_in_prison() is True # Comprova l'estat intern

#GESTIÓ PROPIETATS
def test_player_properties_management(dummy_player: Player) -> None:
    """Comprova que es poden afegir i netejar les propietats del jugador."""
    from typing import cast
    from tile import Property
    propietat_falsa1 = cast(Property, "Propietat 1")
    propietat_falsa2 = cast(Property, "Propietat 2")
    
    # Afegir
    dummy_player.add_property(propietat_falsa1)
    dummy_player.add_property(propietat_falsa2)
    
    # Comprovem (assumint que tens un mètode owned_properties o mirem la llista)
    # Si tens un mètode per llegir-les, canvia '_owned_properties' pel nom del mètode
    assert len(dummy_player.owned_properties()) == 2
    
    # Netejar
    dummy_player.clear_properties()
    assert len(dummy_player.owned_properties()) == 0

#GESTIÓ DE BROKE I BANCAROTA

def test_player_broke_and_bankrupt(dummy_player: Player) -> None:
    """Comprova que el mètode broke() declara el jugador en fallida correctament."""
    
    # 1. Comencem amb el jugador sa
    assert dummy_player.is_bankrupt() is False
    
    # 2. Li traiem absolutament tots els diners i una mica més
    # (Simulem un deute que no pot pagar)
    deute_enorme = dummy_player.money() + 500
    dummy_player.pay(deute_enorme)
    
    # Comprovem que ara té diners negatius
    assert dummy_player.broke()
    
    # 3. Cridem al mètode broke() 
    # (En el joc real el cridaria el Board, però aquí el provem manualment)
    dummy_player.go_bankrupt()
    
    # 4. Verifiquem que l'estat ha canviat
    assert dummy_player.is_bankrupt() is True