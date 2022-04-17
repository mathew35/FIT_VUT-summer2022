## Interpret XML reprezentácia kodu
# autor: Matúš Vráblik
# login: xvrabl05
##

import sys

from handler import *
from argparser import arg
from xmlchecker import xmlcontrol

#argparse
# - spracuje argumenty zadané pri spustení a vráti štruktúru XML strom a štandardný vstup
tree, sys.stdin = arg.argparse(sys.argv,sys.stdin)

#xmlcheck
# - skontroluje XML reprezentáciu kódu a vráti pole s instrukciami a do premennej triedy "instructionHandler" uloží pole s náveštiami pre skokové inštrukcie
instHandler = instructionHandler()
instructions, instHandler = xmlcontrol.xmlcheck(tree,instHandler)

#handle instructions
# - Interpretuje vsetky instrukcie jednu za druhou a po vykonaní každej inštrukcie vráti hodnotu dalšej inštrukcie v poli.
# - Táto hodnota i je ovplyvnená skokovými inštrukciami.
i = 0
while i<len(instructions):
    i = instHandler.handle(instructions[i],i)