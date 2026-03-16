import pytest
from board import Board
from player import Player
from tile import Street, Property, Station, Utility, tax, special
from strategies import Simple_Strategy
from typing import cast

@pytest.fixture
def test_board() -> Board:
    """Fixture que retorna un Board simulat."""
    return cast(Board, None)

@pytest.fixture
def real_board():
    class imaginary_dice:
        def current_dice(self):
                return (1, 1)
    return imaginary_dice()

@pytest.fixture
def owner(test_board: Board) -> Player:
    """Fixture del propietari. Fixa't que rep 'test_board' com argument."""
    return Player(test_board, "Owner", "Barret", "Groc", 0, Simple_Strategy())

@pytest.fixture
def visitor(test_board: Board) -> Player:
    """Fixture del propietari. Fixa't que rep 'test_board' com argument."""
    return Player(test_board, "Visitor", "Barret", "Groc", 0, Simple_Strategy())

@pytest.fixture
def test_street(test_board: Board) -> Street:
    """Fixture del carrer. També rep 'test_board' com argument."""
    # Preu: 350, Lloguer base: 35
    return Street(test_board, 37, "Park Lane", "property", "dark_blue", 350, 
                  35, 70, 175, 500, 1100, 1300, 1500, 200, 200, 175)

# --- TESTS ---

def test_street_buy_logic(test_street: Street, owner: Player) -> None:
    """Comprova que el mètode buy() executa els 3 passos."""
    diners_inicials = owner.money()
    preu_carrer = test_street.price
    
    # ACCIÓ
    test_street.buy(owner)
    
    # COMPROVACIONS
    assert owner.money() == diners_inicials - preu_carrer
    # He posat owner() amb parèntesis si és un getter, o sense si és atribut
    assert test_street.owner == owner 
    assert test_street in owner.owned_properties()

def test_street_on_land_rent_payment(test_board: Board, test_street: Street, owner: Player) -> None:
    """Comprova el pagament del lloguer quan un visitant hi cau."""
    # 1. PREPARACIÓ
    test_street.buy(owner)
    
    # Creem el visitant. Aquí test_board ja és l'objecte, no la funció.
    visitor = Player(test_board, "visitor", "Cotxe", "Roig", 1, Simple_Strategy())
    
    diners_amo_abans = owner.money()
    diners_visitant_abans = visitor.money()
    lloguer_esperat = test_street.rent # El primer valor de la teva llista de lloguers
    
    # 2. ACCIÓ
    test_street.land_on(visitor) # Assegura't que el mètode es diu land_on o on_land
    
    # 3. COMPROVACIÓ
    assert visitor.money() == diners_visitant_abans - lloguer_esperat
    assert owner.money() == diners_amo_abans + lloguer_esperat

# --- 1. TEST DE PROPIETATS BÀSIQUES I HIPOTEQUES ---

def test_property_mortgage_flow(test_board: Board, owner: Player):
    """Cobreix can_mortgage, do_mortgage, can_unmortgage, do_unmortgage i availability."""
    prop = Property(test_board, 1, "Generic", "property", 200, 20, 100, "Desc")
    
    # Comprovar disponibilitat inicial
    assert prop.availability() is True
    
    prop.buy(owner)
    assert prop.availability() is False
    
    # Hipotecar
    assert prop.can_mortgage() is True
    prop.do_mortgage()
    assert prop.is_mortgaged is True
    
    # Intentar hipotecar ja hipotecat
    assert prop.can_mortgage() is False
    
    # Deshipotecar (Paga mortgage + 10%)
    assert prop.can_unmortgage() is True
    prop.do_unmortgage()
    assert prop.is_mortgaged is False

# --- 2. TEST DE STREET (Monopoli i Edificació) ---

def test_street_building_restrictions(test_board: Board, owner: Player):
    """Cobreix monopoli i construcció de cases/hotels."""
    # Creem el set complet de color brown
    s1 = Street(test_board, 1, "Brown 1", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s2 = Street(test_board, 3, "Brown 2", "property", "brown", 60, 4, 8, 20, 60, 180, 320, 450, 50, 50, 30)
    
    s1.buy(owner)
    s2.buy(owner) # Ara té monopoli
    
    # Comprovem que podem edificar les 4 cases una a una
    for _ in range(4):
        # Primer construïm a S1, després a S2 per mantenir l'equilibri
        if s1.can_build_house():
            s1.build_house()
        if s2.can_build_house():
            s2.build_house()

    assert s1.houses == 4
    assert s2.houses == 4
    
    assert s1.can_build_house() is False # Límit de cases assolit
    
    # Ara comprovem l'hotel
    assert s1.can_build_hotel() is True
    s1.build_hotel()
    
    assert s1.hotels == 1
    assert s1.houses == 0
    assert s1.rent_calculation() == 250 # rent_with_hotel (rent[6])

def test_street_selling_buildings(test_board: Board, owner: Player):
    """Cobreix la venda legal de cases i hotels de forma anivellada i controla els diners."""
    # 1. PREPARACIÓ: Necessitem el set complet per poder edificar
    # Preu casa/hotel = 50. Retorn per venda = 25.
    s1 = Street(test_board, 1, "Brown 1", "property", "brown", 60, 2, 4, 10, 30, 90, 160, 250, 50, 50, 30)
    s2 = Street(test_board, 3, "Brown 2", "property", "brown", 60, 4, 8, 20, 60, 180, 320, 450, 50, 50, 30)
    s1.buy(owner)
    s2.buy(owner)
    
    # Forcem monopoli per evitar problemes de mock
    
    # 2. CONSTRUCCIÓ: Pugem a hotel (anivellat)
    for _ in range(4):
        s1.build_house()
        s2.build_house()
    s1.build_hotel()
    s2.build_hotel()
    
    # 3. VENDA D'HOTEL: Comprovem que es pot vendre
    assert s1.can_sell_hotel() is True
    diners_abans_vendre_hotel = owner.money()
    s1.sell_hotel()
    
    # Al vendre l'hotel, recuperes la meitat del cost (50 // 2 = 25)
    assert s1.hotels == 0
    assert s1.houses == 4
    assert owner.money() == diners_abans_vendre_hotel + 25
    
    # 4. VENDA DE CASES (Anivellada)
    # Venem l'hotel de s2 per estar a 4-4 i recuperar 25€ més
    diners_abans_vendre_hotel_s2 = owner.money()
    s2.sell_hotel()
    assert owner.money() == diners_abans_vendre_hotel_s2 + 25
    
    # Ara que estan 4-4, venem una casa de s1
    assert s1.can_sell_house() is True
    diners_abans_vendre_casa = owner.money()
    s1.sell_house()
    
    assert s1.houses == 3
    assert owner.money() == diners_abans_vendre_casa + 25 # Recupera 25€ de la casa
    
    # Si intentem vendre una altra casa de s1 (quedaria 3-4), 
    # mirem si l'anivellament ens obliga a vendre primer la de s2 (per baixar a 3-3)
    if not s1.can_sell_house():
        assert s2.can_sell_house() is True
        diners_abans_vendre_casa_s2 = owner.money()
        s2.sell_house()
        assert s2.houses == 3
        assert owner.money() == diners_abans_vendre_casa_s2 + 25

# --- 3. TEST DE CLASSES ESPECÍFIQUES (Station i Utility) ---

def test_station_calculation(test_board: Board, owner: Player):
    """Cobreix lloguer escalat d'estacions."""
    st1 = Station(test_board, 5, "S1", "station", 200, 25, 100, 50, 100, 200)
    st2 = Station(test_board, 15, "S2", "station", 200, 25, 100, 50, 100, 200)
    
    st1.buy(owner)
    assert st1.rent_calculation() == 25
    
    st2.buy(owner)
    assert st1.rent_calculation() == 50

def test_utility_dice_and_multiplier(real_board: Board, owner: Player, visitor: Player):
    """Cobreix Utility amb daus forçats i multiplicador de carta."""
    ut = Utility(real_board, 12, "Electric", "utility", 150, 75, "Desc", 4, 10)
    ut.buy(owner)
    
    # Forçar daus a (5, 5) -> Suma 10
    real_board.current_dice = lambda: (5, 5)
    
    # 1. Càlcul normal (10 * 4 = 40)
    assert ut.rent_calculation() == 40
    
    # 2. Càlcul via land_on amb multiplicador de carta (Ex: paga x10 la tirada)
    diners_abans = visitor.money()
    ut.land_on(visitor, rent_multiplier=10) # 10 suma * 10 carta = 100
    assert visitor.money() == diners_abans - 100

# --- 4. TEST DE CASSELLES D'ACCIÓ (Tax i Special) ---

def test_tax_and_special_tiles(test_board: Board, owner: Player):
    """Comprova que les taxes resten diners i les caselles especials funcionen."""
    # 1. TAXES: Verifiquem que resten diners
    t = tax(test_board, 4, "Income Tax", "tax", "Desc", 200)
    diners_abans = owner.money()
    t.land_on(owner)
    assert owner.money() == diners_abans - 200
    
    # 2. GO TO JAIL: Verifiquem que el jugador acaba a la presó
    s = special(test_board, 30, "Go To Jail", "special", "Desc")
    
    # Simplement mirem com està el jugador abans i després
    # (Ajusta 'is_in_jail' al nom real que tinguis al teu codi)
    s.land_on(owner)
    
    # Aquí l'assert depèn de com hagis programat Player:
    # Opció A (si tens el mètode):
    assert owner.is_in_prison() is True

# --- 5. TEST DE LAND_ON (Property) ---

def test_property_land_on_cases(test_board: Board, owner: Player, visitor: Player):
    """Cobreix casos de land_on: hipotecat, mateix propietari, etc."""
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