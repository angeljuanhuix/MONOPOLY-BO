import pytest
from board import Board
from player import Player
from tile import Street, Property, Station, Utility, tax, special
from strategies import Simple_Strategy
from typing import cast
import os

@pytest.fixture
def real_board2() -> Board:
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
def test_board() -> Board:
    """Retorna un taulell fals"""
    return cast(Board, None)

@pytest.fixture
def owner(test_board: Board) -> Player:
    """Retorna un player que farà de propietari"""
    return Player(test_board, "Jordi", "🚘", "LightCoral", 0, Simple_Strategy())

@pytest.fixture
def visitor(test_board: Board) -> Player:
    """Retorna un player que farà de visitant"""
    return Player(test_board, "Mireia", "🐧", "LightBlue", 0, Simple_Strategy())

@pytest.fixture
def test_street(test_board: Board) -> Street:
    """Retorna un carrer fals"""
    # Price: 350, rent: 35
    return Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 
                  35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175)

# TEST DE DISPONIBILITAT I HIPOTEQUES

def test_property_mortgage(test_board: Board, owner: Player) -> None:
    """
    Comprova la disponibilitat de la casella i totes
    les funcions relacionades amb hipotèques
    """
    prop = Property(test_board, 1, "Generic", "property", 200, 20, 100, "Description") # Ens inventem un exemple de propietat
    
    # Comprova disponibilitat inicial
    assert prop.availability() is True
    
    prop.buy(owner)
    assert prop.availability() is False
    
    # Hipoteca
    assert prop.can_mortgage() is True
    prop.do_mortgage()
    assert prop.is_mortgaged is True
    
    # Comprovació que no es pot hipotecar si ja ho està
    assert prop.can_mortgage() is False
    
    # Comprova tot el funcionament de deshipotecar
    assert prop.can_unmortgage() is True
    prop.do_unmortgage()
    assert prop.is_mortgaged is False

# TEST STREET

def test_street_buy_logic(test_street: Street, owner: Player) -> None:
    """Comprova que el mètode buy() executa els 3 passos correctament"""
    
    diners_inicials = owner.money()
    preu_carrer = test_street.price
    
    
    test_street.buy(owner)
    
    assert owner.money() == diners_inicials - preu_carrer
    assert test_street.owner == owner 
    assert test_street in owner.owned_properties()

def test_street_on_land_rent_payment(test_street: Street, owner: Player, visitor: Player) -> None:
    """Comprova el pagament del lloguer quan un visitant hi cau."""
    
    # Es fa que el propietari compri el carrer perquè sigui el propietari
    test_street.buy(owner)
    
    old_money_owner = owner.money()
    old_money_visitor = visitor.money()
    rent = test_street.rent 
    
    # El visitor cau a la casella
    test_street.land_on(visitor) 
    
    # Es comprova que s'ha fet el pagament correctament
    assert visitor.money() == old_money_visitor - rent
    assert owner.money() == old_money_owner + rent

def test_street_building_restrictions_and_rent_with_houses(test_board: Board, owner: Player) -> None:
    """
    Comprova la declaració de monopoli i 
    la construcció uniforme d'hotels i cases.
    """
    # Es crea el monopoli marró. (rentWithHotel = 250)
    s1 = Street(test_board, 1, "Old Kent Road", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s2 = Street(test_board, 3, "Whitechapel Road", "property", "brown", 60, 4, 8, 20, 60, 180, 320, 450, 50, 50, 30)
    
    # Owner té el monopoli
    s1.buy(owner)
    s2.buy(owner) 
    
    # Sense cases -> lloguer amb monopoli
    assert s1.rent_calculation() == 4

    # Comprovació de construcció uniforme
    for _ in range(4):
        if s1.can_build_house():
            s1.build_house()
        if s2.can_build_house():
            s2.build_house()

    assert s1.houses == 4
    assert s2.houses == 4
    
    # 4 cases -> lloguer amb 4 cases
    assert s1.rent_calculation() == 160

    assert s1.can_build_house() is False # Límit de cases assolit
    
    # Comprovació de construcció d'hotel
    assert s1.can_build_hotel() is True
    s1.build_hotel()
    
    assert s1.hotels == 1
    assert s1.houses == 0
    assert s1.rent_calculation() == 250 #Comprovació rent_calculation funciona correctament

def test_street_selling_buildings(test_board: Board, owner: Player) -> None:
    """
    Comprova la venda uniforme d'hotels i cases i també
    que s'afegeixin correctament els diners al capital del jugador"""

    # Owner té el monopoli
    s1 = Street(test_board, 1, "Old Kent Road", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s2 = Street(test_board, 3, "Whitechapel Road", "property", "brown", 60, 4, 8, 20, 60, 180, 320, 450, 50, 50, 30)
    s1.buy(owner)
    s2.buy(owner)
    
    # Es construeixen cada hotel en el seu carrer
    for _ in range(4):
        s1.build_house()
        s2.build_house()
    s1.build_hotel()
    s2.build_hotel()
    
    # Es comprova que es vengui l'hotel
    assert s1.can_sell_hotel() is True
    diners_abans_vendre_hotel = owner.money()
    s1.sell_hotel()
    
    # Owner li donen la meitat del preu d'un hotel (50/2 = 25)
    assert s1.hotels == 0
    assert s1.houses == 4
    assert owner.money() == diners_abans_vendre_hotel + 25
    
    # Es comprova que es vengui segon hotel
    diners_abans_vendre_hotel_s2 = owner.money()
    s2.sell_hotel()
    assert owner.money() == diners_abans_vendre_hotel_s2 + 25 #(50/2 = 25)
    

    assert s1.can_sell_house() is True
    diners_abans_vendre_casa = owner.money()
    s1.sell_house()
    
    assert s1.houses == 3
    assert owner.money() == diners_abans_vendre_casa + 25 # Recupera 25€ de la casa
    
    # Es comprova que la venda ha de ser uniforme, no poden haver-hi més dos cases de diferència entre carrers
    assert s1.can_sell_house() is False
    assert s2.can_sell_house() is True
    diners_abans_vendre_casa_s2 = owner.money()
    s2.sell_house()
    assert s2.houses == 3
    assert owner.money() == diners_abans_vendre_casa_s2 + 25

# TEST STATION/UTILITY (ja que tenen un rent_calculation especial)

def test_station_calculation(test_board: Board, owner: Player) -> None:
    """
    Comprova que el preu del lloguer és correcte
    en funció de les estacions que té el propietari
    """
    st1 = Station(test_board, 5, "Kings Cross Station", "station", 200, 25, 100, 50, 100, 200)
    st2 = Station(test_board, 15, "Marylebone Station", "station", 200, 25, 100, 50, 100, 200)
    st3 = Station(test_board, 25, "Fenchurch St Station", "station", 200, 25, 100, 50, 100, 200)
    st4 = Station(test_board, 35, "Liverpool Street Station", "station", 200, 25, 100, 50, 100, 200)
    
    st1.buy(owner)
    assert st1.rent_calculation() == 25
    
    st2.buy(owner)
    assert st1.rent_calculation() == 50

    st3.buy(owner)
    assert st1.rent_calculation() == 100

    st4.buy(owner)
    assert st1.rent_calculation() == 200

def test_utility_dice_and_multiplier(real_board2: Board, owner: Player, visitor: Player) -> None:
    """
    Comprova que el càlcul del lloguer és correcte (depenent de la 
    quantitat d'utilities i si cau a la casella per culpa d'una carta o no)
    """
    
    ut1 = Utility(real_board2, 12, "Electric Company", "utility", 150, 75, "Desc", 4, 10)
    ut2 = Utility(real_board2, 28, "Water Works", "utility", 150, 75, "Desc", 4, 10)
    
    ut1.buy(owner)
    
    # Es simula que es treu dos cincs en els daus
    setattr(real_board2, 'current_dice', lambda: (5, 5))
    
    # Càlcul tenint una utility
    assert ut1.rent_calculation() == 40
    
    # Càlcul si cau per culpa d'una carta (el multiplicador és 10)
    old_money = visitor.money()
    ut1.land_on(visitor, rent_multiplier=10) 
    assert visitor.money() == old_money - 100

    # Càlcul tenint dues utilities
    ut2.buy(owner)
    assert ut1.rent_calculation() == 100

# TEST TAX/SPECIAL

def test_tax_and_special_tiles(test_board: Board, owner: Player) -> None:
    """
    Comprova que les taxes cobren i les special 
    fan la seva funció correctament"""
    
    # Comprovació que tax resta diners
    t = tax(test_board, 4, "Income Tax", "tax", "Desc", 200)
    diners_abans = owner.money()
    t.land_on(owner)
    assert owner.money() == diners_abans - 200
    
    # Es comprova que el jugador vagi a la presó si cau a Go To Jail
    s = special(test_board, 30, "Go To Jail", "special", "Desc")
    s.land_on(owner)
    
    assert owner.is_in_prison() is True

# TEST PROPERTY

def test_property_land_on(test_board: Board, owner: Player, visitor: Player) -> None:
    """Comprova si funciona correctament el land_on del Property"""
    prop = Property(test_board, 1, "Test", "property", 200, 20, 100, "Desc")
    prop.buy(owner)
    
    # Si l'amo cau a casa seva, no paga
    diners_owner = owner.money()
    prop.land_on(owner)
    assert owner.money() == diners_owner
    
    # Si està hipotecada, el visitant no paga
    prop.do_mortgage()
    diners_visitor = visitor.money()
    prop.land_on(visitor)
    assert visitor.money() == diners_visitor

# TEST CHANCE and COMMUNITY CHEST

def test_chance_land_on(real_board2: Board) -> None:
    """
    Comprova la gestió de les cartes CHANCE (que tornin al seu lloc) 
    i si no ha tornat, és perquè era un "get out of jail" card
    """

    import random
    random.seed(42)  # fixem la seed per saber quina carta sortirà
    player = real_board2.players()[0]
    chance_tile = real_board2.tiles()[7]
    
    cards_before = real_board2.chance_deck().cards()[0]  # primera carta del piló
    
    chance_tile.land_on(player)
    
    # Comprova que la carta s'ha mogut al final del piló
    assert real_board2.chance_deck().cards()[-1] == cards_before or player.get_out_of_jail_free_cards() > 0

def test_community_chest_land_on(real_board2: Board) -> None:
    """
    Comprova la gestió de les cartes COMMUNITY_CHEST (que tornin al seu lloc) 
    i si no ha tornat, és perquè era un "get out of jail" card
    """
    import random
    random.seed(42)
    player = real_board2.players()[0]
    community_tile = real_board2.tiles()[2]
    
    cards_before = real_board2.community_chest_deck().cards()[0]
    
    community_tile.land_on(player)
    
    # Comprova que la carta s'ha mogut al final del piló
    assert real_board2.community_chest_deck().cards()[-1] == cards_before or player.get_out_of_jail_free_cards() > 0