#!/usr/bin/env python3
# Do souboru, nazvaného podle konvence isj_proj6_xnovak00.py, implementujte třídu Polynomial, která bude pracovat s polynomy reprezentovanými pomocí seznamů.
# Například 2x^3 - 3x + 1 bude  reprezentováno jako [1,-3,0,2] (seznam začíná nejnižším řádem, i když se polynomy většinou zapisují opačně).

def sign(num):
    if num >=0:
        return '+'
    return '-'

class Polynomial:
    x = []
    ret = ''
    def __init__(self,*args, **kwargs):
        self.values = []
        for i in args:
            if isinstance(i, list):
                self.values = i
        if len(self.values) == 0:
            if args:
                self.values = list(args)
            else:
                for name, value in kwargs.items():
                    for i in range(1 + int(name.split('x')[1]) - len(self.values)):
                        self.values.append(0)
                    self.values[int(name.split('x')[1])]=value
        for i in range(len(self.values)-1,0,-1):
            if self.values[i] == 0:
                del self.values[i]
            else:
                break
    def __str__(self):
        self.ret=""
        if len(self.values)==1:
            self.ret=self.ret+str(self.values[0])
            return self.ret
        for i in reversed(range(len(self.values))):
            if self.values[i]==0:
                continue
            if self.ret:
                if self.values[i]>0:
                    self.ret+= " + "
                else:
                    self.ret+= " - "
            if i==0:
                self.ret+= "{0}".format(str(abs(int((self.values[0])))))
                return self.ret
            if i==1:
                if abs(self.values[1]) == 1:
                    self.ret+= "x"
                else:
                    self.ret+= "{0}x".format(str(abs(int(self.values[1]))))
            else:
                if abs(self.values[i]) == 1:
                    self.ret+= "x^{0}".format(i)
                else:
                    self.ret+= "{0}x^{1}".format(str(abs(int(self.values[i]))), i)
        return self.ret
    def __eq__(self,other):
        if len(self.values) != len(other.values):
            return False
        zipped = zip(self.values,other.values)
        for val1,val2 in zipped:
            if val1 != val2:
                return False
        return True
    def __add__(self,other):
        tmp = self.values[:]
        i = 0
        for val1,val2 in zip(self.values,other.values):
            tmp[i]= val1 + val2
            i += 1
        if len(self.values) < len(other.values):
            for i in range(len(self.values),len(other.values)):
                tmp.append(other.values[i])
        return Polynomial(tmp)
    def __pow__(self,power):
        if power == 0:
            if len(self.values)==1 and self.values[0]==0:
                raise ValueError("0^0")
            return Polynomial(1)
        if power == 1:
            return Polynomial(self.values)
        if power > 1:
            tmp = self
            power1 = power
            i = power1
            for i in range(1,power):
                tmp = tmp * self
            power1 = i
            return Polynomial(tmp)
        if power < 0:
            raise ValueError("power < 0")
        return Polynomial()
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
    def at_value(self,x_1, x_2=None):
        ret = 0
        for i in reversed(range(len(self.values))):
            ret = (ret*x_1)+self.values[i]
        if x_2:
            retx = 0
            for i in reversed(range(len(self.values))):
                retx = (retx*x_2)+self.values[i]
            ret = retx - ret
        return ret
# Instance třídy bude možné vytvářet několika různými způsoby:
# pol1 = Polynomial([1,-3,0,2])
# pol2 = Polynomial(1,-3,0,2)
# pol3 = Polynomial(x0=1,x3=2,x1=-3)
# Volání funkce print() vypíše polynom v obvyklém formátu:

# >>> print(pol2)
# 2x^3 - 3x + 1

# Bude možné porovnávat vektory porovnávat:
# >>> pol1 == pol2
# True

# Polynomy bude možné sčítat a umocňovat nezápornými celými čísly:
# >>> print(Polynomial(1,-3,0,2) + Polynomial(0, 2, 1))
# 2x^3 + x^2 - x + 1
# >>> print(Polynomial(-1, 1) ** 2)
# x^2 - 2x  + 1

# A budou fungovat metody derivative() - derivace a at_value() - hodnota polynomu pro zadané x - obě pouze vrací výsledek, nemění samotný polynom:
# >>> print(pol1.derivative())
# 6x^2 - 3
# >>> print(pol1.at_value(2))
# 11
# >>> print(pol1.at_value(2,3))
# 35

# (pokud jsou zadány 2 hodnoty, je výsledkem rozdíl mezi hodnotou at_value() druhého a prvního parametru - může sloužit pro výpočet určitého integrálu, ale ten nemá být implementován)

# Maximální hodnocení bude vyžadovat, abyste:
# - uvedli "shebang" jako v předchozích projektech
# - důsledně používali dokumentační řetězce a komentovali kód
# - nevypisovali žádné ladicí/testovací informace při běžném "import isj_proj6_xnovak00"
# - zajistili, že následující platí:
def test():
    # print(str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)))
    assert str(Polynomial(0,1,0,-1,4,-2,0,1,3,0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    # print(str(Polynomial(-5,1,0,-1,4,-2,0,1,3,0)))
    assert str(Polynomial([-5,1,0,-1,4,-2,0,1,3,0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3= -1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2,0,3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    # print(str(Polynomial(x0=1)+Polynomial(x1=1)))
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
    