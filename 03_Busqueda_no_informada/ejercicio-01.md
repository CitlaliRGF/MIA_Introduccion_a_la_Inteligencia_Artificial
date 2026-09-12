# Ejercicio 01 — Comparar BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

## Origen-destino y diagrama del subgrafo

La pareja utilizada fue: `Timisoara` → `Bucharest`

Lo que dio origen al siguiente diagrama del subgrafo:

```text


                         ┌── 99 km ──> Fagaras ──211 km──> Bucharest
                         │
Timisoara ─118─> Arad ─140─> Sibiu
                         │
                         └── 80 km ──> Rimnicu Vilcea ─97─> Pitesti ─101─> Bucharest
```


## Tabla comparativa


| Algoritmo         | Path                                                            | Depth |   Cost | Expanded | Status  |
| ----------------- | --------------------------------------------------------------- | ----: | -----: | -------: | ------- |
| **BFS**           | Timisoara → Arad → Sibiu → Fagaras → Bucharest                  |     4 | 568 km |        7 | success |
| **UCS**           | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest |     5 | 536 km |       12 | success |
| **DFS**           | Timisoara → Arad → Sibiu → Fagaras → Bucharest                  |     4 | 568 km |        4 | success |
| **DLS (limit=3)** | —                                                               |     — |      — |        6 | cutoff  |
| **DLS (limit=4)** | Timisoara → Arad → Sibiu → Fagaras → Bucharest                  |     4 | 568 km |        4 | success |
| **IDS**           | Timisoara → Arad → Sibiu → Fagaras → Bucharest                  |     4 | 568 km |       14 | success |



## Reporte

Al comparar los diferentes algoritmos usando la ruta de `Timisoara` a `Bucharest`, pude notar que BFS y UCS buscan algo diferente. BFS sí encontró el camino con menos carreteras, ya que llegó a Bucharest utilizando 4 carreteras y recorriendo 568 km. En cambio, UCS encontró el camino con menos kilómetros, con un total de 536 km, aunque utilizó 5 carreteras. Esto se debe a que BFS se enfoca en encontrar la solución con menor profundidad, mientras que UCS toma en cuenta el costo acumulado de cada camino.

En el caso de DFS, también encontró el camino de 4 carreteras y 568 km en esta prueba. Sin embargo, esto no significa que siempre encuentre el mejor camino. DFS va avanzando lo más profundo posible por una rama antes de regresar y probar otras opciones. Por eso, dependiendo del orden en que explore los nodos, puede encontrar primero un camino que sea más largo o tenga un mayor costo, aunque exista otra ruta mejor en el mismo grafo.

Finalmente, con DLS, al utilizar --limit 3 el resultado fue cutoff, porque no podía llegar hasta Bucharest. Al aumentar el límite a --limit 4, encontró la solución de 4 carreteras y 568 km. Esto tiene relación directa con BFS e IDS, ya que ambos encontraron una solución con profundidad 4. En el caso de IDS, fue justamente con limit=4 cuando encontró la solución. Esto muestra que el límite de DLS debe ser al menos igual a la profundidad necesaria para llegar a la solución.
