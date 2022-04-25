#!/usr/bin/env python3
# Do souboru, nazvaného podle konvence isj_proj6_xnovak00.py, implementujte třídu Polynomial, která bude pracovat s polynomy reprezentovanými pomocí seznamů.
# Například 2x^3 - 3x + 1 bude  reprezentováno jako [1,-3,0,2] (seznam začíná nejnižším řádem, i když se polynomy většinou zapisují opačně).
from numpy import polymul


def sign(x):
    if x >=0:
        return '+'
    return '-'

class Polynomial:
    x = []
    ret = ''
    def __init__(self,*args, **kwargs):
        self.values = list()
        for i in args:
            if type(i) is list:
                self.values = i
        if len(self.values) == 0:
            if args:
                self.values = list(args)
            else:
                for xY, value in kwargs.items():
                    for i in range(1 + int(xY.split('x')[1]) - len(self.values)):
                        self.values.append(0)
                    self.values[int(xY.split('x')[1])]=value
        for i in range(len(self.values)-1,0,-1):
            if self.values[i] == 0:
                del self.values[i]
            else:
                break
    def __str__(self):
        rev = self.values[::-1]
        self.ret=''
        count = len(self.values)-1
        for k in range(len(rev)):
            i = rev[k]
            if type(i) == type(Polynomial(5)):
                self.ret = str(i);
                continue
            if i != 0:
                if self.ret == '':
                    if abs(i)>1:# and count >1:
                        self.ret = str(i)#+"x^"+str(count)
                        if count > 1:
                            self.ret = self.ret+"x^"+str(count)
                        elif count == 1:
                            self.ret = self.ret+"x"
                    elif abs(i)==1:
                        if count > 1:
                            self.ret = "x^"+str(count)
                        elif count == 1:
                            self.ret = "x"
                    
                elif abs(i)>1 and count>1:
                    self.ret = self.ret+" "+sign(i)+" "+str(abs(i))+"x^"+str(count)
                elif abs(i)>1 and count==1:
                    self.ret = self.ret+" "+sign(i)+" "+str(abs(i))+"x"
                elif abs(i)==1 and count>1:
                    self.ret = self.ret+" "+sign(i)+" "+"x^"+str(count)
                elif abs(i)==1 and count==1:
                    self.ret = self.ret+" "+sign(i)+" "+"x"
                elif abs(i)>0 and count >0:
                    self.ret = self.ret+" "+sign(i)+" "+"x"
                elif abs(i)>0:
                    self.ret = self.ret+" "+sign(i)+" "+str(abs(i))
            count -= 1
        if self.ret == '':
            self.ret = '0'
        return self.ret
    def __eq__(self,other):
        if len(self.values) != len(other.values):
            return False
        zipped = zip(self.values,other.values)
        for x,y in zipped:
            if x != y:
                return False
        return True
    def __add__(self,other):
        tmp = self.values[:]
        i = 0
        for x,y in zip(self.values,other.values):
            tmp[i]= x + y
            i += 1
        if len(self.values) < len(other.values):
            for i in range(len(self.values),len(other.values)):
                tmp.append(other.values[i])
        return Polynomial(tmp)
    def __pow__(self,power):
        if power == 0:
            if len(self.values)==1 and self.values[0]==0:
                raise ValueError("0^0")
            else:
                return 1
        if power == 1:
            return Polynomial(self.values)
        if power > 1:
            tmp = self
            for i in range(1,power):
                tmp = tmp * self
            return Polynomial(tmp)
        if power < 0:
            raise ValueError("power < 0")
    def __mul__(self,other):
        tmp = [0] * (len(self.values)+len(other.values)+1)
        for i in range(len(self.values)):
            for j in range(len(other.values)):
                tmp[i+j] = self.values[i]*other.values[j]+tmp[i+j]
        return Polynomial(tmp)
    def derivative(self):
        tmp = self.values[:]
        if len(tmp) == 1:
            return 0
        del tmp[0]
        for i in range(len(tmp)):
            tmp[i] = tmp[i] * (i + 1)
        return Polynomial(tmp)        
    def at_value(self,x1, x2=None):
        ret = 0
        for i in reversed(range(len(self.values))):
            ret = (ret*x1)+self.values[i]
        if x2:
            retx = 0
            for i in reversed(range(len(self.values))):
                retx = (retx*x2)+self.values[i]
            ret = retx - ret
        return ret
# Instance třídy bude možné vytvářet několika různými způsoby:
pol1 = Polynomial([1,-3,0,2])
pol2 = Polynomial(1,-3,0,2)
pol3 = Polynomial(x0=1,x3=2,x1=-3)
"""
# Volání funkce print() vypíše polynom v obvyklém formátu:

>>> print(pol2)
2x^3 - 3x + 1

# Bude možné porovnávat vektory porovnávat:
>>> pol1 == pol2
True

# Polynomy bude možné sčítat a umocňovat nezápornými celými čísly:
>>> print(Polynomial(1,-3,0,2) + Polynomial(0, 2, 1))
2x^3 + x^2 - x + 1
>>> print(Polynomial(-1, 1) ** 2)
x^2 - 2x  + 1

# A budou fungovat metody derivative() - derivace a at_value() - hodnota polynomu pro zadané x - obě pouze vrací výsledek, nemění samotný polynom:
>>> print(pol1.derivative())
6x^2 - 3
>>> print(pol1.at_value(2))
11
>>> print(pol1.at_value(2,3))
35
"""
# (pokud jsou zadány 2 hodnoty, je výsledkem rozdíl mezi hodnotou at_value() druhého a prvního parametru - může sloužit pro výpočet určitého integrálu, ale ten nemá být implementován)

# Maximální hodnocení bude vyžadovat, abyste:
# - uvedli "shebang" jako v předchozích projektech
# - důsledně používali dokumentační řetězce a komentovali kód
# - nevypisovali žádné ladicí/testovací informace při běžném "import isj_proj6_xnovak00"
# - zajistili, že následující platí:
def test():
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1)+Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1,1,1,0])+Polynomial(1,-1,1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(pol1+pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1,x1=1)**1) == "x - 1"
    assert str(Polynomial(x0=-1,x1=1)**2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1,x1=1)
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3**4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2,x1=3,x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2,x1=3,x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2,3,4,-5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3,5) == 44
    pol5 = Polynomial([1,0,-2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1,3.6) == -23.92
    assert pol5.at_value(-1,3.6) == -23.92

if __name__ == '__main__':
    test()
    