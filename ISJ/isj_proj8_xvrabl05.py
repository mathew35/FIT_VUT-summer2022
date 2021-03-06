#!/usr/bin/env python3
# Do souboru, nazvaného podle konvence isj_proj8_xnovak00.py, definujte generátorovou
# funkci first_with_given_key, která bude mít 2 parametry - povinný parametr iterable,
# odpovídající předanému iterovatelnému objektu (může být i nekonečný), a dále nepovinný
# parametr key, odpovídající funkci, která při volání na položce objektu iterable vrátí
# hodnotu klíče, s defaultní hodnotou identické funkce (tedy vrácení přímo položky, na
# které je funkce zavolána), implementované pomocí konstrukce lambda. Funkce aplikuje 
# klíč na položky objektu iterable a vybírá (generuje) pouze ty, jejichž klíč se dosud
# nevyskytl. V případě potřeby pamatovat si nehashovatelné objekty použijte funkci repr.
# Například:
def first_with_given_key(iterable,key=lambda a: a):
    iterate = iter(iterable)
    ret = list()
    while True:
        try:
            item = next(iterate)
            if key(item) not in ret:
                yield item
                ret.insert(-1, key(item))
        except StopIteration:
            break
print(tuple(first_with_given_key([[1],[2,3],[4],[5,6,7],[8,9]], key = len)))
# vypíše 
# ([1], [2, 3], [5, 6, 7]).