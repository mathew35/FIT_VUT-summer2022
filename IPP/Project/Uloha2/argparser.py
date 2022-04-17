## Interpret XML reprezentácia kodu
# autor: Matúš Vráblik
# login: xvrabl05
##

import xml.etree.ElementTree as ET
import sys
class arg:
    #argparse() - skontroluje argumenty a pokúsi sa otvorit zadané súbory a uloziť ich obsah v adekvátnej forme
    #           - vrácia tree typu xml.etree.ElementTree a IN predstavujúcu STDIN alebo príslišný súbor
    def argparse(args,IN):
        if(len(args) < 2):
            exit(10)
            
        if args[1] == '--help':
            print("Usage: interpret.py [--help | --source=file | --input=file] [options]")
            print("       --help          show this help")
            print("\n       Use at least one of the following (other will be read from STDIN if needed):")
            print("       --source=<file> input file with XML representation of source code")
            print("       --input=<file>  file of user inputs for interpretation")
            exit(0)

        argparser={
                '--source': 1,
                '--input': 2
            }
        tree = None

        for i in args[1:]:
            i = i.split('=')
            arg1 = argparser.get(i[0],0)

            if not arg1:
                exit(10)

            if arg1 == 1:
                if tree != None:
                    exit(10)
                try:
                    open(i[1])
                except:
                    exit(11)
                try:
                    tree = ET.parse(i[1])
                except:
                    exit(31)

            if arg1 == 2:
                try:
                    IN = open(i[1])
                except:
                    exit(11)
                    
        if tree == None:
                try:
                    tree = ET.parse(sys.stdin)
                except:
                    exit(31)
        return tree, IN