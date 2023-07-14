# Solitario Klondike

Esta es una implementación del juego de cartas Solitario Klondike, también conocido como *Solitaire* o *Patience*. El juego se ejecuta en la terminal, y se puede jugar con el teclado. Incluye también un par *solvers* que resuelven el juego automáticamente utilizando DFS y *deep Q-learning*.

La implementación del modelo DQN fue desarrollada originalmente por Michael Richardson, licenciada bajo la versión 3 de la GPL y que se puede encontrar en [este repositorio](https://github.com/xkiwilabs/DQN-using-PyTorch-and-ML-Agents).

## Cómo ejecutar

Para ejecutar el juego, es necesario tener instalado Python 3.7 o superior. Con Python instalado, basta con ejecutar el siguiente comando:

```console
$ ./main.py
```

Los siguientes son algunos ejecutables asociados a los *solvers* implementados:

- `./viewer.py <tablero>`: muestra el tablero especificado (en formato JSON) en una ventana gráfica, pudiendo reproducir las jugadas realizadas por el *solver* DFS
- `./dfs_solver.py`: resuelve el juego con el algoritmo de búsqueda en profundidad con un tablero inicial aleatorio
    - `./dfs_solver.py <tablero>`: resuelve el juego con el algoritmo de búsqueda en profundidad con el tablero especificado (en formato JSON)
    - `./dfs_solver.py --bench`: resuelve el juego con el algoritmo de búsqueda en profundidad con 1000 tableros iniciales aleatorios, generando estadísticas
    - `./dfs_solver.py --bench <tablero1> <tablero2> ...`: resuelve el juego con el algoritmo de búsqueda en profundidad iterativamente con los tableros especificados (en formato JSON), generando estadísticas
    - Cada vez que el algoritmo encuentra una solución, guarda en la carpeta `boards/` un archivo JSON con el tablero inicial y la secuencia de jugadas que lleva a la solución.
- `./rl_train.py`: entrena un agente de refuerzo usando *deep Q-learning*, generando un modelo PyTorch y estadísticas
    - `./rl_train.py <tablero1> <tablero2> ...`: entrena un agente de refuerzo usando *deep Q-learning* con los tableros especificados (en formato JSON)
    - El entrenamiento se ejecutará hasta alcanzar una tasa de 75% de victorias. En cualquier momento, se puede detener el entrenamiento con `Ctrl+C`, y se guardará el modelo y las estadísticas hasta ese momento. También se genera un archivo que contiene la semilla del generador de números aleatorios, para poder reproducir el entrenamiento.
- `./rl_test.py <modelo> <semilla>`: resuelve el juego con un agente de refuerzo entrenado, generando estadísticas.
    - El modelo corresponde al archivo PTH generado por el entrenamiento. La semilla corresponde al valor contenido el archivo de semilla generado por el entrenamiento.
- `./generate_boards.py <n>`: genera `n` tableros iniciales aleatorios, guardándolos en la carpeta `boards/random/` en formato JSON

## Cómo jugar

En cada jugada, se imprime por pantalla el estado actual del tablero, y se pide al usuario que introduzca una jugada. Los movimientos válidos son los siguientes:

- `m <a> <b> [<size>]`: mueve la carta superior de la pila `a` a la pila `b`. Si se especifica `size`, se moverán tantas cartas como se indique. Por defecto, se mueve una sola carta.
- `d <a>`: saca una carta del depósito y la pone en el descarte
- `f <a>`: mueve la última carta de la columna `a` a su casilla correspondiente en la base
- `w <a>`: mueve la última carta de la columna `a` al descarte
- `s`: mueve la última carta del descarte a su casilla correspondiente en la base
- `b <a> <b>`: mueve la última carta de la base `a` a la columna `b`
- `u`: deshace la última jugada
- `q`: sale del juego

Si alguno de los comandos o las jugadas que generan no son válidas, se imprime un mensaje de error y se vuelve a pedir una jugada.

## Integrantes

- Aníbal Ibaceta
- Sebastián Hevia
- Jorge Jara
