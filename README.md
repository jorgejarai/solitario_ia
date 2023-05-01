# Solitario Klondike

## Cómo ejecutar

```console
$ ./main.py
```

## Cómo jugar

En cada jugada, se imprime por pantalla el estado actual del tablero, y se pide al usuario que introduzca una jugada. Los movimientos válidos son los siguientes:

- `m <a> <b> [<size>]`: mueve la carta superior de la pila `a` a la pila `b`. Si se especifica `size`, se moverán tantas cartas como se indique. Por defecto, se mueve una sola carta.
- `d <a>`: saca una carta del depósito y la pone en el descarte
- `f <a>`: mueve la última carta de la columna `a` a su casilla correspondiente en la base
- `w <a>`: mueve la última carta de la columna `a` al descarte
- `s`: mueve la última carta del descarte a su casilla correspondiente en la base
- `b <a> <b>`: mueve la última carta de la base `a` a la columna `b`
- `q`: sale del juego

Si alguno de los comandos o las jugadas que generan no son válidas, se imprime un mensaje de error y se vuelve a pedir una jugada.
