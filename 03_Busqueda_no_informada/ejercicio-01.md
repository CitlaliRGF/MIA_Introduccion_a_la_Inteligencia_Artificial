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


```

<svg xmlns="http://www.w3.org/2000/svg"
     width="1100"
     height="500"
     viewBox="0 0 1100 500">

  <defs>
    <marker id="arrow"
            markerWidth="10"
            markerHeight="10"
            refX="9"
            refY="3"
            orient="auto"
            markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 Z" fill="#333"/>
    </marker>
  </defs>

  <!-- Título -->
  <text x="550" y="35"
        text-anchor="middle"
        font-family="Arial"
        font-size="24"
        font-weight="bold">
    Subgrafo relevante: Timisoara → Bucharest
  </text>

  <!-- Aristas -->
  <g stroke="#333"
     stroke-width="2"
     fill="none"
     marker-end="url(#arrow)">

    <!-- Camino común -->
    <line x1="100" y1="250" x2="270" y2="250"/>
    <line x1="320" y1="250" x2="490" y2="250"/>

    <!-- Rama BFS / DFS / DLS / IDS -->
    <line x1="540" y1="250" x2="700" y2="130"/>
    <line x1="750" y1="130" x2="930" y2="130"/>

    <!-- Rama UCS -->
    <line x1="540" y1="250" x2="700" y2="370"/>
    <line x1="750" y1="370" x2="850" y2="370"/>
    <line x1="900" y1="370" x2="1030" y2="370"/>
  </g>

  <!-- Etiquetas de distancias -->
  <g font-family="Arial"
     font-size="16"
     font-weight="bold"
     fill="#333">

    <text x="180" y="235">118 km</text>
    <text x="390" y="235">140 km</text>

    <text x="605" y="165">99 km</text>
    <text x="820" y="115">211 km</text>

    <text x="605" y="345">80 km</text>
    <text x="790" y="350">97 km</text>
    <text x="955" y="350">101 km</text>
  </g>

  <!-- Nodos -->
  <g font-family="Arial"
     font-size="16"
     text-anchor="middle">

    <circle cx="100" cy="250" r="40" fill="white" stroke="#333" stroke-width="2"/>
    <text x="100" y="255">Timisoara</text>

    <circle cx="320" cy="250" r="40" fill="white" stroke="#333" stroke-width="2"/>
    <text x="320" y="255">Arad</text>

    <circle cx="530" cy="250" r="40" fill="white" stroke="#333" stroke-width="2"/>
    <text x="530" y="255">Sibiu</text>

    <circle cx="730" cy="130" r="40" fill="white" stroke="#333" stroke-width="2"/>
    <text x="730" y="135">Fagaras</text>

    <circle cx="970" cy="130" r="50" fill="white" stroke="#333" stroke-width="2"/>
    <text x="970" y="125">Bucharest</text>
    <text x="970" y="145" font-size="13">(BFS / DFS / DLS / IDS)</text>

    <circle cx="730" cy="370" r="50" fill="white" stroke="#333" stroke-width="2"/>
    <text x="730" y="365">Rimnicu</text>
    <text x="730" y="385">Vilcea</text>

    <circle cx="875" cy="370" r="40" fill="white" stroke="#333" stroke-width="2"/>
    <text x="875" y="375">Pitesti</text>

    <circle cx="1030" cy="370" r="50" fill="white" stroke="#333" stroke-width="2"/>
    <text x="1030" y="365">Bucharest</text>
    <text x="1030" y="385" font-size="13">(UCS)</text>
  </g>

  <!-- Leyenda -->
  <g font-family="Arial" font-size="15">
    <text x="550" y="460" text-anchor="middle">
      Rama superior: BFS, DFS, DLS e IDS — 568 km, 4 carreteras
    </text>
    <text x="550" y="485" text-anchor="middle">
      Rama inferior: UCS — 536 km, 5 carreteras
    </text>
  </g>

</svg>

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