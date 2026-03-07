# PROJECTE MONOPOLY 2026
En aquest README podrà trobar les explicacions de tots aquells canvis importants en el meu codi i també podrà veure la estrategia que s'ha emprat per fer el projecte i la seva metologia.

# ÍNDEX
* [Creació del current_dice (1)](#creació-del-current_dice-1)


## Creació del current_dice (1)
S'ha creat un mètode nou a part del ``dice()`` que es situa al ``board.py`` El motiu de la seva creació és per guardar el nombre que surt en el dau, perquè s'ha vist que el ``draw.py()`` per veure el nombre que s'ha tret torna a cridar al ``dice()`` i si en aquest mètode és on generem el nombre, doncs es genera per primera vegada quan decidim quants passos fa el jugador i una altra vegada per mostrar en pantalla el nombre dels daus cosa que provoca que no concordi el nombre de caselles que es mou la fitxa i els nombres que surten en els daus.


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

## JOCS DE PROVES (SEEDS)