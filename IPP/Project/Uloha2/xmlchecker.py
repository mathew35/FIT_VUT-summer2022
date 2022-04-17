## Interpret XML reprezentácia kodu
# autor: Matúš Vráblik
# login: xvrabl05
##

import numpy
import re
class xmlcontrol:
    # Kontrola XML reprezentácie zdrojového kódu a nájdenie naveští pre skoky
    #   Vracia pole inštrukcií a upravenú premennú pre spracovanie inštrukcií
    def xmlcheck(tree, instHandler):  
        # slovník OP kódov s príslušným počtom argumentov ako hodnotou       
        opcodes = {"CREATEFRAME":0,"PUSHFRAME":0,"POPFRAME":0,"RETURN":0,"BREAK":0,"DEFVAR":1,
                "POPS":1,"PUSHS":1,"WRITE":1,"EXIT":1,"DPRINT":1,"CALL":1,"LABEL":1,"JUMP":1,"MOVE":2,
                "NOT":2,"INT2CHAR":2,"TYPE":2,"STRLEN":2,"READ":2,"ADD":3,"SUB":3,"MUL":3,"IDIV":3,"LT":3,
                "GT":3,"EQ":3,"AND":3,"OR":3,"STRI2INT":3,"CONCAT":3,"GETCHAR":3,"SETCHAR":3,
                "JUMPIFEQ":3,"JUMPIFNEQ":3,"DIV":3,"INT2FLOAT":2,"FLOAT2INT":2,"CLEARS":0,"ADDS":0,"SUBS":0,
                "MULS":0,"IDIVS":0,"LTS":0,"GTS":0,"EQS":0,"ANDS":0,"ORS":0,"NOTS":0,"INT2CHARS":0,"STRI2INTS":0,
                "JUMPIFEQS":1,"JUMPIFNEQS":1}
        # pole možných hodnôt atribútu "type" u argumentov instrukcií
        types = {'var','int','string','bool','nil','float','type','label'}
        # Element program - kontrola hlavného elementu 'program' a jeho vyžiadaných atribútov
        root=tree.getroot()
        if root.tag != "program":
            exit(32)
        if root.get('language',None) != "IPPcode22":
            exit(32)
        # Element instruction - kontrola instrukcií a ich vyžiadaných atribútov
        instr = {}
        for i in root:
            if i.tag != "instruction":
                exit(32)
            order = i.get("order",None)
            if not order:
                exit(32)
            if int(order) < 1:
                exit(32)
            if not re.match('[0-9]+',order) or int(order)<1 :
                exit(32)
            if instr.get(int(i.get("order"),0)) != None:
                exit(32)
            if i.get("opcode") == None:
                exit(32)
            if not i.get("opcode").upper() in opcodes:
                exit(32)
            # Element argX - kontrola argumentov a ich vyžiadaných atribútov
            args = {}
            for arg in i:
                if not arg.get("type") in types:
                    exit(32)
                if args.get(arg.tag,0):
                    exit(32)
                if not re.match('^arg[0-9]+$',arg.tag):
                    exit(32)
                matches = re.search('\\\[0-9]{3}',arg.text)
                # Nahradenie spatného lomítka a 3 nasledujúcich čísel respektívnym ascii znakom
                if matches:
                    k = 0
                    matches = matches.group()
                    arg.text = re.sub('\\\[0-9]{3}',chr(int(matches[1:])),arg.text)
                # Uloženie argumentu do slovníka argumentov s tagom xml elementu ako kľúčom a samotným argumentom ako hodnotou
                args[arg.tag]=arg
            # Kontrola existencie OPCODE
            k = len(args)
            if k!= opcodes[i.get("opcode").upper()]:
                exit(32)
            # Kontrola počtu argumentov pre daný OPCODE
            while k != 0 :
                argName = 'arg'+str(k)
                if not argName in args:
                    exit(32)
                k = k - 1
            # Priradenie slovníka args do pola instrukcií s atribútom order ako indexom
            instr[int(i.get("order"))] = (i.get("opcode").upper(),sorted(args.items()))
        # Zmena indexov pola instrukcií na nasledujúce: [0,1,2,3,...,n]
        instr = numpy.array(sorted(instr.items()))
        # Prvé prejdenie inštrukcií a uloženie náveští do pola náveští premennej instHandler
        i = 0
        while i<len(instr):
            instr[i][0]=i
            if instr[i][1][0] == 'LABEL':
                if instr[i][1][1][0][1].text in instHandler.labs:
                    exit(52)
                instHandler.labs[instr[i][1][1][0][1].text] = i
            i = i + 1
        return instr, instHandler