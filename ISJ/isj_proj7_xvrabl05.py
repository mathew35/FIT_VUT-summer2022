#!/usr/bin/env python3
# Do souboru, nazvaného podle konvence isj_proj7_xnovak00.py, implementujte funkci (decorator factory) log_and_count,
#     která umožní použití dekorátoru s určením jména key (klíče ve struktuře Counter), pod kterou má být volání dané
#     funkce započítáno, nebo použije jako klíč následující jméno funkce. Druhým parametrem, který bude muset být zadán
#     s klíčovým jménem counts, bude jméno struktury Counter, do níž má být počítání ukládáno. Mělo by tedy fungovat
#     následující:

import collections

my_counter = collections.Counter()

def log_and_count(*argsouter,**kwargsouter):
    def decorators(func):
        def inner(*args,**kwargs):
            if 'key' in kwargsouter:
                kwargsouter['counts'][kwargsouter['key']] += 1
            elif argsouter:
                print(argsouter)
                kwargsouter['counts'][list(argsouter)[0]] += 1
            else:
                kwargsouter['counts'][func.__name__] += 1
            print("called "+str(func.__name__)+" with "+str(args)+" and "+str(kwargs))
            return func(*args, **kwargs)
        return inner
    return decorators

@log_and_count(key = 'basic functions', counts = my_counter)
def f1(a, b=2):
    return a ** b

@log_and_count(key = 'basic functions', counts = my_counter)
def f2(a, b=3):
    return a ** 2 + b

@log_and_count(counts = my_counter)
def f3(a, b=5):
    return a ** 3 - b

f1(2)
f2(2, b=4)
f1(a=2, b=4)
f2(4,5)
f2(5)
f3(5)
f3(5,4)

# a vypíše postupně:
# called f1 with (2,) and {}
# called f2 with (2,) and {'b': 4}
# called f1 with () and {'a': 2, 'b': 4}
# called f2 with (4,) and {}
# called f2 with (5,) and {}
# called f3 with (5,) and {}
# called f3 with (5, 4) and {}

# a po:
print(my_counter)
# vypíše
# Counter({'basic functions': 5, 'f3': 2})
