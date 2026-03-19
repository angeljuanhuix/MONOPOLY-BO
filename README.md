# PROJECTE MONOPOLY 2026 🎲
Aquest projecte tracta sobre la creació d'un monopoli totalment funcional, amb algunes diferències respecte el joc original. El joc es mostra en un html a part gràcies a la creació d'imatges .svg que representen cada acció i moviment de tota la partida. Aquest README serveix per consultar qualsevol dubte que es tingui respecte al projecte.

# Índex
- **[Requeriments](#requeriments)**
- **[Com s'executa el joc](#com-sexecuta-el-joc)**
- **[Com visualitzar el joc](#com-visualitzar-el-joc)**
- **[Estructura del projecte](#estructura-del-projecte)**
- **[Decisions de disseny](#decisions-de-disseny)**
- **[Canvis respecte al joc original](#canvis-respecte-al-joc-original)**
- **[Testing](#testing)**

## Requeriments
Cal instal·lar la llibreria ``drawsvg``:

**CODI:** ``python3 -m pip install drawsvg``

## Com s'executa el joc
1. Situa't a la carpeta ``PROJECTE_MONOPOLY``
2. Executa el ``main.py`` (Clicant a ▶️ o escrivint a la terminal ``python CODIS/main.py``)
3. Introdueix el nombre de jugadors (2-4) quan t'ho demani la terminal.

El joc crearà les imatges a la carpeta ``images`` dins de ``CODIS`` 
## Com visualitzar el joc
1. Situa't dins ``PROJECTE_MONOPOLY\CODIS``
2. Executa a la terminal: ``python3 slideshow.py partida.html (ls images/imatge*.svg)`` o ``python3 slideshow.py partida.html $(Get-ChildItem images/*.svg)`` 

Si utilizes MAC, prova el següent codi: ``python3 slideshow.py partida.html images/imatge*.svg``

3. Obre el fitxer ``partida.html`` per veure la partida

**ATENCIÓ!⚠️**

Hi ha la possibilitat que salti un error quan s'intenten visualitzar moltes imatges (Problema de Windows). Si per mala sort et salta, visualitza la partida manualment des del VS Code.

## Estructura del projecte
<pre>
PROJECTE_MONOPOLY/
├── CODIS/
│   ├── main.py          # Executor del joc
│   ├── board.py         # Taulell i lògica principal del joc
│   ├── tile.py          # Caselles del taulell
│   ├── player.py        # Jugadors
│   ├── card.py          # Targetes de Chance i Community Chest
│   ├── deck.py          # Baralles de targetes
│   ├── strategies.py    # Estratègies dels jugadors automàtics
│   ├── draw.py          # Generació d'imatges SVG
│   ├── slideshow.py     # Visualitzador HTML de la partida
│   ├── const.py         # Constants del joc
│   └── images/          # Imatges SVG generades
└── JSON/
    ├── tiles.json           # Dades de les caselles
    ├── players.json         # Dades dels jugadors
    ├── chance.json          # Targetes de Chance
    └── community-chest.json # Targetes de Community Chest
</pre>

## Decisions de disseny
### ```tile.py```
Com indica l'objectiu del projecte, s'ha utilitzat **l'herència** i el **polimorfisme** amb una "classe pare" anomenada Tile. L'estructura de les caselles és la següent:
<pre>
Tile (base)
├── Property
│   ├── Street
│   ├── Station
│   └── Utility
├── chance
├── community_chest
├── tax
└── special
</pre>
A ``Property`` hi ha un ``land_on`` que és el que s'usarà en general en tots els tipus de propietats. Però, gràcies al **POLIMORFISME**, cada tipus té un ``rent_calculation`` amb el seu propi càlcul de lloguer. El que s'aconsegueix amb això, és que des del ``land_on`` es crida ``self.rent_calculation()`` per calcular el lloguer del tipus de propietat que hagi caigut el jugador.

***PER QUÈ S'HA IMPLEMENTAT UN MULTIPLIER EN EL ``land_on``?***

Per defecte és 1 perquè no afecti el càlcul del lloguer, però el multiplier s'utilitza per quan un jugador cau en una **estació o utility** per culpa d'una targeta *chance o community chest*, ja que la targeta imposa un multiplicador del lloguer.

***PER QUÈ ``Utility`` TÉ UN ``land_on`` PARTICULAR?***

Perquè la targeta indica que el multiplicador ha de ser **x10** independentment de quantes utilities tingui. És diferent que les estacions on només s'havia de multiplicar el resultat final.

### ``strategies.py``
Els jugadors automàtics faran una acció o un altre gràcies a la classe ``Strategy``. Cada estratègia conté un ``desire_of...`` que retorna un booleà indicant si es vol fer aquella acció o no.

**TIPUS D'ESTRATÈGIES:**

- ``Simple_Strategy``: Sempre compra i mai construeix res
- ``Smart_Strategy``: Compra mantenint un coixí (``MINIMUM_MONEY``), hipoteca si baixa del mínim i deshipoteca quan té prous diners(``UNMORTGAGE_MONEY``)

**DETALL IMPORTANT☝🏻:**
Hi ha mètodes en el ``tile.py`` que diuen ``can_...``, aquests retornen un booleà segons les *normes del joc* i el ``desire_of_...`` segons *l'estratègia*

### ``board.py``
**SISTEMA DE DAUS**

S'ha creat un mètode auxiliar pels daus anomenat ``dice`` que retorna el nombre de l'última tirada i el ``current_dice`` tira els daus (genera nombres) i retorna el resultat.

El ***motiu*** és perquè en el ``draw.py``, per dibuixar el valors dels daus agafava ``current_dice`` i com aquesta funció genera nous nombres cada vegada que es crida, doncs no coincidirien el nombres de caselles que el jugador es mou i els nombres que surten en els daus.

**FRAMES EXTRES**

Es generen frames extres en els següents casos:

- **Utility amb propietari:** Es mostra una altra tirada pel càlcul del lloguer
- **Chance/Community Chest:** Es mostra l'execució de la carta a més a més de quan el jugador hi cau
- **Go To Jail:** Mostra que el jugador cau a la casella i en el següent frame és a *la presó*

**GESTIÓ DE FALLIDA**

Quan un jugador queda amb ***diners negatius*** després d'un ``land_on``:

- Totes les *propietats* tornen **al banc**
- Les *targetes per sortir de la presó* tornen a **baix del piló** d'allà on s'han agafat inicialment
- El jugador es *marca* com ``is_bankrupt = True`` i els diners es posen a 0$
- *Les peces* dels jugadors es queden **allà on ha mort**
- El *jugador* es queda **visible** tota la partida

**TARGETES DE SORTIDA DE PRESÓ**

S'ha creat un mètode ``set_deck()`` per assignar d'on ve la targeta i poder-la tornar a deixar en el piló que toca després del seu *ús o declaració de fallida.*

**CONSTRUCCIÓ UNIFORME**

S'ha tingut en compte en tot moment la **construcció uniforme:** no es pot construir una casa en un carrer si les altres tenen menys.

Es gestiona en el ``can_build`` del ``Street``, que recorre tots els carrers del mateix color i comprova si aquell carrer té menys cases que els altres carrers (en el cas contrari no deixaria construir).

També, relacionat amb la **construcció uniforme**, en el ``board.py``, dins de ``post_movement_actions()`` es fan múltiples passades amb el ``while action_done`` per garantir que es construeixi tantes vegades com sigui possible, sempre respectant *la construcció uniforme.*

**CANVI EN LES CONSTANTS**

S'han modificat les constants a ``const.py`` perquè les partides siguin més **dinàmiques** i durin menys frames. Per tant, perquè els jugadors amb una *estratègia simple* **NO comprin** tant i permetin els jugadors automàtics *més llestos* aconseguir monopolis, s'han implementat aquests canvis:

- **Go Salary:** 200$ -> 50$
- **Start Money:** 1500$ -> 750$


## Canvis respecte al joc original
Per simplificar el procés de creació del projecte, s'han fet alguns canvis respecte les normes oficials dels jocs:

- **NO** es poden subhastar les propietats
- S'han modificat els diners inicials 
- S'han modificat els diners que reben quan passen pel **GO**
- **NO** es pot sortir de la presó pagant *50$* ni s'ha de pagar quan es surt amb el tercer torn
- Quan es cau en *fallida*, **totes les propietats** van al *banc* i poden tornar a ser comprades
- **NO** es poden fer *tractes, ni intercanvis entre jugadors*

## Testing 
***COVERAGE ACONSEGUIT:*** *93,16%🔋* (sense comptar el ``board.py``)

(No s'ha comptat el ``board.py``, ja que s'hi *dibuixen les imatges* i no es vol que es creïn noves imatges mentres es fan testos i per tant, com no ha estat testejat tant exhaustivament, té un percentatge baix.)

Els tests es troben dins de la carpeta ``/CODIS`` amb els noms ``test_board``, ``test_card``, ``test_player``, ``test_strategies``, ``test_tile``.

Per executar-ho segueix els següents passos:

1. Situar-se a ``PROJECTE_MONOPOLY/CODIS`` 
2. A la banda esquerra, s'haurà de clicar en una icona semblant a un **matràs d'erlenmeyer**. 
3. Situar-se sobre "PROJECTE_MONOPOLY" i en teoria hi ha de veure tres ▶️, doncs cliqui el tercer que posa *"Run test with coverage"*. 

Fent això es mostren el % de línies comprovades amb els testos

**EINES UTILITZADES**

- ``pytest``: Marc de treball per fer proves
- ``@pytest.fixture``: Permet crear objectes de prova reutilitzables (board, player, ...) i s'inicialitzen automàticament a cada test
- ``os.path``: Per indicar la ruta dels JSON 
- ``cast()``: Utilitzat en alguns testos. El que fa és dir que una variable és de cert tipus, per exemple, s'ha fet que ``test_board = cast(Board, None)`` perquè així no es tinguin problemes amb el mypy i no s'hagi de crear un board sencer per provar coses que *no* necessita el board.


