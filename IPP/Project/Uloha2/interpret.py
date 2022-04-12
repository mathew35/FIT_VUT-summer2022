import xml.etree.ElementTree as ET
import sys
import re

import numpy
from handler import *



#argparse
if(len(sys.argv) < 1):
    exit(10)
if sys.argv[1] == '--help':
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
for i in sys.argv[1:]:
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
            sys.stdin = open(i[1])
        except:
            exit(11)
#xmlcheck
opcodes = {"CREATEFRAME":0,"PUSHFRAME":0,"POPFRAME":0,"RETURN":0,"BREAK":0,"DEFVAR":1,
           "POPS":1,"PUSHS":1,"WRITE":1,"EXIT":1,"DPRINT":1,"CALL":1,"LABEL":1,"JUMP":1,"MOVE":2,
           "NOT":2,"INT2CHAR":2,"TYPE":2,"STRLEN":2,"READ":2,"ADD":3,"SUB":3,"MUL":3,"IDIV":3,"LT":3,
           "GT":3,"EQ":3,"AND":3,"OR":3,"STRI2INT":3,"CONCAT":3,"GETCHAR":3,"SETCHAR":3,
           "JUMPIFEQ":3,"JUMPIFNEQ":3,"DIV":3,"INT2FLOAT":2,"FLOAT2INT":2,"CLEARS":0,"ADDS":0,"SUBS":0,
           "MULS":0,"IDIVS":0,"LTS":0,"GTS":0,"EQS":0,"ANDS":0,"ORS":0,"NOTS":0,"INT2CHARS":0,"STRI2INTS":0,
           "JUMPIFEQS":1,"JUMPIFNEQS":1}
types = {'var','int','string','bool','nil','float','type','label'}
root=tree.getroot()
if root.tag != "program":
    exit(32)
if root.get('language',None) != "IPPcode22":
    exit(32)
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
    args = {}
    for arg in i:
        if not arg.get("type") in types:
            exit(32)
        if args.get(arg.tag,0):
            exit(32)
        if not re.match('^arg[0-9]+$',arg.tag):
            exit(32)
        matches = re.search('\\\[0-9]{3}',arg.text)
        if matches:
            k = 0
            matches = matches.group()
            arg.text = re.sub('\\\[0-9]{3}',chr(int(matches[1:])),arg.text)
        args[arg.tag]=arg
    k = len(args)
    if k!= opcodes[i.get("opcode").upper()]:
        exit(32)
    while k != 0 :
        argName = 'arg'+str(k)
        if not argName in args:
            exit(32)
        k = k - 1
    instr[int(i.get("order"))] = (i.get("opcode").upper(),sorted(args.items()))
instr = numpy.array(sorted(instr.items()))
i = 0
instHandler = instructionHandler()
while i<len(instr):
    instr[i][0]=i
    if instr[i][1][0] == 'LABEL':
        if instr[i][1][1][0][1].text in instHandler.labs:
            exit(52)
        instHandler.labs[instr[i][1][1][0][1].text] = i
    i = i + 1
#print(instr)
#interpret
i = 0
while i<len(instr):
#for i  in instr:
    #i[0] = order
    #i[1] = args
    ##for n in i[1]:
        #n[0] = arg$num
        #n[1] = Element arg$num
        ##print(n[1],end='')
    ##print()
    i = instHandler.handle(instr[i],i)
    #print(gbz.GF,"main GF")
# print("ok")