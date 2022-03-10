# Server v jazyku C komunikujúci prostredníctvom protokolu HTTP

## Autor : Matúš Vráblik

### Popis
Lightweit server ktory dokaze uzivatelovi poskytnut nasledovne:
* meno serveru
* model procesoru
* zátaž procesoru

### Spustenie
Stiahni a extrahuj zazipovaný server
V adresáry servera ho prelož príkazom:
```
$ make
```
Spusti aplikáciu na porte <port>:
```
$ ./hinfosvc <port>
```

### Priklady pouzitia
Ak je problém s volaním "GET" použi "curl"
```
$ GET http://localhost:<port>/hostname
$ GET http://localhost:<port>/cpu-name
$ GET http://localhost:<port>/load
```