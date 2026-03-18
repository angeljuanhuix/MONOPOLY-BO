# PROJECTE MONOPOLY 2026
En aquest README podrà trobar les explicacions de tots aquells canvis importants en el meu codi i també podrà veure la estrategia que s'ha emprat per fer el projecte i la seva metologia.

# ÍNDEX
* [Creació del current_dice (1)](#creació-del-current_dice-1)


## Creació del current_dice (1)
S'ha creat un mètode nou a part del ``dice()`` que es situa al ``board.py`` El motiu de la seva creació és per guardar el nombre que surt en el dau, perquè s'ha vist que el ``draw.py()`` per veure el nombre que s'ha tret torna a cridar al ``dice()`` i si en aquest mètode és on generem el nombre, doncs es genera per primera vegada quan decidim quants passos fa el jugador i una altra vegada per mostrar en pantalla el nombre dels daus cosa que provoca que no concordi el nombre de caselles que es mou la fitxa i els nombres que surten en els daus.

## CONSTRUCCIÓ UNIFORME

## DIFERÈNCIES AMB JOC ORIGINAL (fixar-me en el canvi de constant)

## REQUERIMENTS (QUÈ T'HAS D'INSTAL·LAR)

## QUÈ PASSA SI UN JUGADOR SE'N VA A LA FALLIDA?
- Les propietats del jugador s'alliberen (tornen al banc).
- Les targetes de sortida de presó tornen a la baralla corresponent.
- El jugador es marca com en fallida i els seus diners es posen a 0.
- Es queden allà on es moren

## COSES A REVISAR
-El can_be_bought. No sé si hauria de ser allà on s'assigna el propietari

## COM CREAR LES IMATGES
1. T'has d'ubicar dins la carpeta AP2\PROJECTE_MONOPOLY
2. Executar el ``main.py``

## COM MOSTRAR IMATGES A L'HTML
1. T'has d'ubicar dins la carperta AP2\PROJECTE_MONOPOLY\CODIS
2. Escriure a la terminal ``python3 slideshow.py partida.html (ls images/imatge*.svg)``

## IMPLEMENTACIÓ TRIA DE QUANTS JUGADORS ES VOLEN JUGAR

## EXPLICAR LO DE @PROPERTY, EXPLICAR 
 
## IMPORTANT, IMPLEMENTAR A L'ESTRATEGIA
No oblidar-me de posar a l'estrategia si un jugador vol construir casa, o vol hipotecar o vol deshipotecar

## RENT_MULTIPLIER DEL LAND_ON
Serveix per quan toca alguna carta i s'ha de multiplicar per dos el lloguer en el cas que sigui d'algú, si no es fa res, doncs serà 1 i no canviarà res

## EXPLICACIÓ PERQUÈ HE POSAT UN LAND_ON A UTILITY
S'ha hagut de fer un land_on en particular per utility perquè en el cas que es caigui a una utility per culpa d'una targeta, el multiplicador per calcular el lloguer serà sempre x10, sense tenir en compte si té una utilitat o dues, cosa que amb la station hem pogut aprofitar el land_on de property perquè es modifica el lloguer final i no el lloguer en si.

## CREACIÓ FRAME EXTRA QUAN ES CAU A UTILITY I A CHANCE/COMMUNITY_CHEST
En el cas d'utility, es fa perquè carreguin els daus i es mostrin per pantalla perquè així el corrector pugui veure perquè s'ha pagat certa quantitat, gràcies a que pot veure el valor dels daus que s'han de tirar per calcular el lloguer

Per chance i community_chest, es fa un frame extra per mostrar el que s'executa amb la carta:
- Moviment(es veurà que el nombre del dau no canvia però el jugador es mou a la casella que li toca)
- Pagar
...

## TESTING
Com en els testos havíem de crear un player de prova o tiles
S'ha utilitzat ``@pytest.fixture`` que serveix per crear-lo una vegada i utilitzant el nom de la seva funció, doncs es carregarà automàticament.

S'ha utilitzat ``cast`` per poder declar que una variable és de x tipus sense que el mypy es queixi.

## TRACTAMENT BANCAROTA
- Es queden quiets a la posició on moren
- Se'ls inicialitza tot a 0
- Totes les propietats van al banc

# FUNCIONS IMPORTANTS 

## `` def play(self) -> None``

- Torns dels jugadors
- Llançament de daus i moviment
- Gestió de dobles (torn extra i tercera doble → presó)
- Sistema de presó (sortida per dobles, targeta o 3 torns)
- Accions post-moviment (construir, hipotecar, vendre)
- Detecció de bancarota
- Canvi de jugador (saltant els que estan en bancarota)
 
La partida acaba quan només queda un jugador actiu o s'arriba al límit de frames.
