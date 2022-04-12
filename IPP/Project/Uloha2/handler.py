global GF
global LF
global TF
global Order
GF = {}
LF = None
TF = None
Order = 0
DataStack = []
CallStack = []
LFStack = []
global Labels
Labels = {}
class variable:
    Type = None
    Value = None
    Float = None
    def set(self,Type,Value):
        self.Type = Type
        self.Value = Value
        if Type == 'float':
            self.Float = True
            self.Value = float.fromhex(Value)
        if Type == 'int':
            self.Value = int(Value)
        if Type == 'bool':
            tmp = False
            if self.Value == 'true':
                tmp = True
            self.Value = tmp
    def copy(self,source):
        self.Type = source.Type
        self.Value = source.Value
        self.Float = source.Float

def getVar(var):
    if var.get("type") == 'var':
        arg = var.text.split('@')
        frame = globals()[arg[0]]
        try:
            foo = arg[1] in frame
        except:
            exit(55)
        if not foo:
            exit(54)
        return frame[arg[1]] 
    return False
def getArg(arg):
    if arg.get("type") == 'var':
        return getVar(arg)
    ret = variable()
    ret.set(arg.get("type"),arg.text);
    return ret
#Prace s ramci, volani funkci
def MOVE(args):
    arg1 = args[0][1].text.split('@')
    if args[1][1].get("type") == 'var':
        arg = args[1][1].text.split('@')
        varT = globals()[arg[0]][arg[1]]
        Type = var.Type
        Value = var.Value
    else:
        Type = args[1][1].get("type")
        Value = args[1][1].text    
    var = globals()[arg1[0]]
    if not arg1[1] in var:
        exit(54)
    var = var[arg1[1]]
    var.set(Type,Value)
def CREATEFRAME(args):
    global TF
    TF = {}
def PUSHFRAME(args):
    global TF
    global LF
    if not TF:
        exit(55)
    LF = TF
    LFStack.append(LF)
    TF = None
def POPFRAME(args):
    global TF
    global LF
    if LF == None:
        exit(55)
    TF = LFStack.pop()
    try:
        LF = LFStack.pop()
        LFStack.append(LF)
    except:
        LF = None
def DEFVAR(args):
    arg = args[0][1].text.split('@')
    frame = globals()[arg[0]]
    try:
        if arg[1] in frame:
            exit(52)
    except:
        exit(55)
    frame[arg[1]] = variable()
def CALL(args):
    global Order
    CallStack.append(Order + 1)
    if not args[0][1].text in Labels:
        exit(52)
    Order = Labels[args[0][1].text]
def RETURN(args):
    global Order
    try:
        Order = CallStack.pop()
    except:
        exit(56)
#Prace s datovym zasobnikem
def PUSHS(args):
    loc = getVar(args[0][1])
    var = variable()
    var.set(args[0][1].get('type'),args[0][1].text)
    if loc:
        var.copy(loc)
    
    DataStack.append(var)
def POPS(args):
    var = getVar(args[0][1])
    try:
        poped = DataStack.pop()
    except:
        exit(56)
    var.copy(poped)
    
#Aritmeticke, relacni, booleovske a konverzni instrukce
def ADD(args):
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if arg1.Type != 'int' or arg2.Type != 'int':
        if arg1.Type != 'float' or arg2.Type != 'float':
            exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = arg1.Type
    var.Value = arg1.Value+arg2.Value
def SUB(args):
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if arg1.Type != 'int' or arg2.Type != 'int':
        if arg1.Type != 'float' or arg2.Type != 'float':
            exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = arg1.Type
    var.Value = arg1.Value-arg2.Value
def MUL(args):
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if arg1.Type != 'int' or arg2.Type != 'int':
        if arg1.Type != 'float' or arg2.Type != 'float':
            exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = arg1.Type
    var.Value = arg1.Value*arg2.Value
def IDIV(args):
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if arg1.Type != 'int' or arg2.Type != 'int':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    if args[2][1].text == '0':
        exit(57)
    var.Type = arg1.Type
    var.Value = arg1.Value/arg2.Value
def LT(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != args[2][1].get("type"):
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = args[1][1].text < args[2][1].text
def GT(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != args[2][1].get("type"):
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = args[1][1].text > args[2][1].text
def EQ(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != args[2][1].get("type"):
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = args[1][1].text == args[2][1].text
def AND(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != 'bool' or args[2][1].get("type") != 'bool':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = args[1][1].text and args[2][1].text
def OR(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != 'bool' or args[2][1].get("type") != 'bool':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = args[1][1].text or args[2][1].text
def NOT(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != 'bool':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    var.Type = Type
    var.Value = not args[1][1].text
def INT2CHAR(args):
    arg1 = getArg(args[1][1])
    var = getVar(args[0][1])
    if arg1.Type != 'int':
        exit(53)
    if not var:
        exit(54)
    try:
        value = chr(int(arg1.Value))
    except:
        exit(58)
    var.Type = 'string'
    var.Value = value
def STRI2INT(args):
    Type = args[1][1].get("type")
    if args[1][1].get("type") != 'string':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    try:
        value = ord(int(args[1][1].text))
    except:
        exit(58)
    var.Type = 'int'
    var.Value = value
#Vstupne-vystupni instrukce
def READ(args):
    Type = args[1][1].text   
    var = getVar(args[0][1])
    if not var:
        exit(54) 
    try:
        Input = input()
    except:
        Type = 'nil'
    Value = None
    if Type == 'bool':
        Value = False
        if Input == 'true':
            Value = True
    if Type == 'string':
        Value = str(Input)
    if Type == 'int':
        Value = int(Input)
    if Type == 'float':
        Value = float.fromhex(Input)
    if Type == 'nil':
        Value = 'nil@nil'
    if Value == None:
        exit(58)
    var.Type = Type
    var.Value = Value
def WRITE(args):
    var = getVar(args[0][1])
    if var :
        Value = var.Value
        Type = var.Type
    else:
        Value = args[0][1].text
        Type = args[0][1].get('type')
        x = variable()
        x.set(Type,Value)
        Value = x.Value
    if Type == 'bool':
        out = 'false'
        if Value:
            out = 'true'
    if Type == 'string':
        out = Value
    if Type == 'int':
        out = int(Value)
    if Type == 'float':
        out = float.hex(Value)
    if Type == 'nil':
        out = ''
    if Value == None:
        out = ''
    print(out,end='')
#Prace s retezci
def CONCAT(args):
    pass
def STRLEN(args):
    pass
def GETCHAR(args):
    pass
def SETCHAR(args):
    pass
#Prace s type
def TYPE(args):
    arg = getArg(args[1][1])
    var = getVar(args[0][1])
    Type = arg.Type
    if Type == 'nil':
        Type = ''
    var.set('string',Type);
#Instrukce rizeni toku
def LABEL(args):
    global Order
    label = args[0][1].text
    Labels[label] = Order
def JUMP(args):
    global Order
    try:
        Order = Labels[args[0][1].text]
    except:
        exit(52)
def JUMPIFEQ(args):
    global Order
    label = args[0][1].text
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if (arg1.Type != arg2.Type):
        if (arg1.Type == 'nil' or arg2.Type == 'nil'):
            Order = Labels[label]
            return
        exit(53)
    if (arg1.Value == arg2.Value):
        try:
            Order = Labels[label]
        except:
            exit(52) 
def JUMPIFNEQ(args):
    global Order
    label = args[0][1].text
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if (arg1.Type != arg2.Type):
        if (arg1.Type == 'nil' or arg2.Type == 'nil'):
            Order = Labels[label]
            return
        exit(53)
    if (arg1.Value != arg2.Value):
        try:
            Order = Labels[label]
        except:
            exit(52) 
def EXIT(args):
    arg1 = getArg(args[0][1])
    if not (0<=arg1.Value and arg1.Value<=49):
        exit(57)
    exit(arg1.Value)
#Ladici instrukce
def DPRINT(args):
    pass
def BREAK(args):
    pass
#FLOAT bonusove rozsireni instrukce
def INT2FLOAT(args):
    var = getVar(args[0][1])
    arg1 = getArg(args[1][1])
    if not var:
        exit(54)
    if not arg1.Type:
        exit(56)    
    if arg1.Type != 'int':
        exit(53)
    var.Type = 'float'
    var.Value = float(arg1.Value)
def FLOAT2INT(args):
    var = getVar(args[0][1])
    arg1 = getArg(args[1][1])
    if not var:
        exit(54)
    if not arg1.Type:
        exit(56)    
    if arg1.Type != 'float':
        exit(53)
    var.Type = 'int'
    var.Value = int(arg1.Value)
def DIV(args):
    arg1 = getArg(args[1][1])
    arg2 = getArg(args[2][1])
    if arg1.Type != 'float' or arg2.Type != 'float':
        exit(53)
    var = getVar(args[0][1])
    if not var:
        exit(54)
    if arg2.Value == 0:
        exit(57)
    var.Type = arg1.Type
    var.Value = arg1.Value/arg2.Value
#STACK bonusove rozsireni instrukce
def CLEARS(args):
    global DataStack
    DataStack = []
def ADDS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != 'float' and arg1.Type != 'int':
        exit(53)
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value + arg2.Value
    DataStack.append(var)
def SUBS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != 'float' and arg1.Type != 'int':
        exit(53)
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value - arg2.Value
    DataStack.append(var)
def MULS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != 'float' and arg1.Type != 'int':
        exit(53)
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value * arg2.Value
    DataStack.append(var)
def IDIVS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != 'float' and arg1.Type != 'int':
        exit(53)
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value / arg2.Value
    DataStack.append(var)
def LTS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = 'bool'
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value < arg2.Value
    DataStack.append(var)
def GTS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = 'bool'
    if arg1.Type != arg2.Type:
        exit(53)
    var.Value = arg1.Value > arg2.Value
    DataStack.append(var)
def EQS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = 'bool'
    if arg1.Type != arg2.Type:
        if arg1.Type != 'nil' and arg2.Type != 'nil':
            exit(53)
    var.Value = arg1.Value == arg2.Value
    DataStack.append(var)
def ANDS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != arg2.Type or arg1.Type != 'bool':
        exit(53)
    var.Value = arg1.Value and arg2.Value
    DataStack.append(var)
def ORS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = arg1.Type
    if arg1.Type != arg2.Type or arg1.Type != 'bool':
        exit(53)
    var.Value = arg1.Value or arg2.Value
    DataStack.append(var)
def NOTS(args):
    try:
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    if arg1.Type != 'bool':
        exit(53)
    var.Type = 'bool'
    var.Value = not arg1.Value
    DataStack.append(var)
def INT2CHARS(args):
    try:
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = 'string'
    if arg1.Type != 'int':
        exit(53)
    try:
        var.Value = chr(arg1.Value)
    except:
        exit(58)
    DataStack.append(var)
def STRI2INTS(args):
    try:
        arg2 = DataStack.pop()
        arg1 = DataStack.pop()
    except:
        exit(56)
    var = variable()
    var.Type = 'int'
    if arg1.Type != 'string' or arg2.Type != 'int':
        exit(53)
    try:
        var.Value = ord(arg1.Value[arg2.Value])
    except:
        exit(58)
    DataStack.append(var)
def JUMPIFEQS(args):
    global Order
    EQS([])
    label = getArg(args[0][1]).Value
    try:
        res = DataStack.pop()
    except:
        exit(56)
    if res.Value:
        try:
            Order = Labels[label]
        except:
            exit(52)
def JUMPIFNEQS(args):
    global Order
    EQS([])
    label = getArg(args[0][1]).Value
    try:
        res = DataStack.pop()
    except:
        exit(56)
    if not res.Value:
        try:
            Order = Labels[label]
        except:
            exit(52)

class instructionHandler:
    global Labels
    labs = Labels
    def handle(self, instr, order):
        global Order
        Order = order + 1
        globals()[instr[1][0]](instr[1][1])
        #print(Labels)
        #print(Order)
        return Order
