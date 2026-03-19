import pytest
from player import Player
from strategies import Strategy, Simple_Strategy
from const import START_MONEY, GO_SALARY, NUM_TILES
from board import Board
from typing import cast
from tile import Property
from card import Card

@pytest.fixture 
def test_player() -> Player:
    
    
    test_board = cast(Board, None) #Fem que el board pugui ser None perquè no s'utilitzarà per testejar el player.py
    return Player(board = test_board , name="Jordi", piece="🚘", color="LightCoral", index=0, strategy = Simple_Strategy())


#ATRIBUTS BÀSICS

def test_player_basic_getters_and_initialization(test_player: Player) -> None:
    """
    Comprova que la inicialització del jugador és correcte i els
    mètodes bàsics funcionen correctament
    """
    
    assert test_player.name() == "Jordi"
    assert test_player.piece == "🚘"
    assert test_player.color() == "LightCoral"
    assert test_player.index() == 0
    assert test_player.board() is None  
    assert isinstance(test_player.strategy(), Strategy)
    assert test_player.position() == 0
    assert test_player.money() == START_MONEY
    assert not test_player.is_in_prison()

#MOVIMENTS

def test_player_normal_move(test_player: Player) -> None:
    """
    Comprova que el jugador es mou correctament
    (No passa per la casella de Sortida)
    """
    
    test_player.move(5, NUM_TILES)
    
    assert test_player.position() == 5
    assert test_player.money() == START_MONEY # Els diners no han de canviar

def test_player_collects_go_salary(test_player: Player) -> None:
    """
    Comprova que si es passa per la casella de sortida,
    se li suma correctament el GO_SALARY
    """
    test_player.set_position(38)
    test_player.move(4, NUM_TILES) 

    #Si es mou 4 caselles des de la 38, hauria d'acabar a la 2
    
    assert test_player.position() == 2 
    assert test_player.money() == START_MONEY + GO_SALARY

#GESTIÓ DE PROPIETATS

def test_player_add_property(test_player: Player) -> None:
    """
    Comprova que s'afegeix correctament una propietat
    quan un jugador la compra
    """
    
    test_property = cast(Property, "Propietat de Prova")
    
    # S'afegeix la propietat inventada a la seva llista de propietats
    test_player.owned_properties().append(test_property) 
    
    assert len(test_player.owned_properties()) == 1
    assert test_player.owned_properties()[0] == test_property

def test_player_properties_management(test_player: Player) -> None:
    """Comprova que es poden afegir i netejar les propietats del jugador."""
    test_property1 = cast(Property, "Propietat 1")
    test_property2 = cast(Property, "Propietat 2")
    
    # S'afegeixen a llista de propietats del jugador
    test_player.add_property(test_property1)
    test_player.add_property(test_property2)
    
    assert len(test_player.owned_properties()) == 2
    
    # Tornem propietats al banc (després de fer bancarota en teoria)
    test_player.clear_properties()
    assert len(test_player.owned_properties()) == 0

#GESTIÓ RELACIONADA AMB LA PRESÓ (Cartes, management...)

def test_player_get_out_of_jail_cards(test_player: Player) -> None:
    """
    Comprova que el jugador rep les targetes
    per sortir de la presó correctament
    """  
    
    test_card = cast(Card, "Get Out of Jail")

    #Abans d'afegir, es comprova que no en tingui cap
    
    assert len(test_player.get_out_of_jail_cards()) == 0
    
    test_player.get_out_of_jail_cards().append(test_card)

    #Després d'afegir, es comprova que en té una
    
    assert len(test_player.get_out_of_jail_cards()) == 1

def test_player_prison_turns_counter(test_player: Player) -> None:
    """
    Comprova que s'afegeixen correctament 
    els torns de la presó i que es poden llegir
    """
    assert test_player.turns_in_prison() == 0
    
    test_player.add_turn_in_prison()
    assert test_player.turns_in_prison() == 1
    
    test_player.add_turn_in_prison()
    assert test_player.turns_in_prison() == 2

def test_player_leave_prison(test_player: Player) -> None:
    """
    Comprova que el jugador surt de la presó correctament
    i canvia el seu esta
    """
    
    # Es suposa que porta dos torns
    test_player.add_turn_in_prison()
    test_player.add_turn_in_prison()
    assert test_player.turns_in_prison() == 2
    
    # Surt per qualsevol motiu (daus dobles, li han passat els torns...)
    test_player.leave_prison()
    
    # Comprovació que es reinicien els torns i l'estat de ser a la presó
    assert test_player.turns_in_prison() == 0
    assert not test_player.is_in_prison()

def test_player_jail_cards_management(test_player: Player) -> None:
    """Comprova el cicle complet de les cartes de sortir de la presó."""
    
    test_card = cast(Card, "Carta Test")
    
    # Comprova que s'agafa correctament
    test_player.add_get_out_of_jail_free_card(test_card)
    assert test_player.get_out_of_jail_free_cards() == 1
    
    # Comprova que s'utilitza (hauria de retornar la carta i treure-la de la llista)
    carta_usada = test_player.use_get_out_of_jail_card()
    assert carta_usada == test_card
    assert test_player.get_out_of_jail_free_cards() == 0
    
    # Comprova que la funció de netejar funciona (quan cau en bancarota s'utilitza la funció)
    test_player.add_get_out_of_jail_free_card(test_card)
    test_player.clear_jail_cards()
    assert test_player.get_out_of_jail_free_cards() == 0

def test_player_go_to_prison(test_player: Player) -> None:
    """Comprova que el mètode d'anar a la presó actualitza l'estat i la posició."""
    test_player.go_to_prison()
    
    assert test_player.position() == 10 # 10 és la casella de la presó
    assert test_player.is_in_prison() is True # Comprova l'estat intern

#GESTIÓ DE BROKE I BANCAROTA

def test_player_broke_and_bankrupt(test_player: Player) -> None:
    """Comprova que el mètode broke() declara el jugador en fallida correctament."""
    
    # Es comprova que el jugador no estigui en fallida
    assert test_player.is_bankrupt() is False
    
    # Es simula que ha de pagar més del que té
    deute_enorme = test_player.money() + 500
    test_player.pay(deute_enorme)
    
    # Es comprova que ara té diners negatius (o sigui que està en fallida)
    assert test_player.broke()
    
    # Com en teoria està en fallida, manualment li indiquem que 
    # es declari que està en fallida
    test_player.go_bankrupt()
    
    # Es verifica que l'estat ha canviat
    assert test_player.is_bankrupt() is True