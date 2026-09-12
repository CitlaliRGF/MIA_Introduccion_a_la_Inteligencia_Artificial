# Comparar Greedy y A* en el mapa de Rumania

## Origen-destino y diagrama del subgrafo

La pareja utilizada fue: `Timisoara` → `Bucharest`

Lo que dio origen al siguiente diagrama del subgrafo:

```text
                       Timisoara
                        h = 329
                    
                    /            \
                 118 km          111 km
                  /                  \
              Arad                  Lugoj
             h=366                   h=244
              |                        |
            140 km                  70 km
              |                        |
            Sibiu                   Mehadia
            h=253                   h=241
              |                       |
            80 km                   75 km
              |                       |
       Rimnicu Vilcea              Drobeta
            h=193                   h=242
              |                      |
            97 km                 120 km
               \                    /
                \                  /
               Pitesti ◄──── Craiova
                h=100           h = 160
                  |
               101 km
                  |
               Bucharest
                 h=0
                        
```




## Tabla comparativa

| Algoritmo         | Path                                                            | Depth |   Cost | Expanded | Heurística  |
| ----------------- | --------------------------------------------------------------- | ----: | -----: | -------: | ------- |
| **Greedy Best-First**           | Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest                  |     6 | 615 km |        6 | straight-line distance to Bucharest (AIMA table) |
| **A* **           | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest |     5 | 536 km |       10 | straight-line distance to Bucharest (AIMA table) |




## Reporte

En esta comparación utilicé como origen `Timisoara` y como destino `Bucharest`. Los dos algoritmos encontraron una solución, pero no llegaron por el mismo camino. A* encontró el camino de menor costo, con 536 km, siguiendo la ruta `Timisoara` → `Arad` → `Sibiu` → `Rimnicu Vilcea` → `Pitesti` → `Bucharest`. En cambio, Greedy tomó otra ruta: `Timisoara` → `Lugoj` → `Mehadia` → `Drobeta` → `Craiova` → `Pitesti` → `Bucharest`, que terminó siendo de 615 km. O sea, Greedy sí llegó al destino, pero se desvió y terminó recorriendo 79 km más.

Esto pasa porque Greedy se enfoca principalmente en `h(n)`, que en este caso es la distancia en línea recta estimada hasta Bucharest. Entonces, básicamente intenta ir siempre hacia la ciudad que parece estar más cerca del objetivo, sin tomar tanto en cuenta cuánto ha costado llegar hasta ahí. Aunque la heurística sea admisible, eso no significa que Greedy vaya a encontrar el camino más barato. La admisibilidad de `h` es importante para A*, pero Greedy no utiliza el costo acumulado `g(n)` de la misma forma. Por eso puede tomar una ruta que parece buena al principio, pero que termina siendo más cara.

En el caso de A*, se utiliza `f(n) = g(n) + h(n)`, por lo que toma en cuenta tanto lo que ya se recorrió como lo que falta aproximadamente. En el camino que encontró, los valores de `f` fueron **329, 484, 511, 531, 535 y 536**, por lo que se observa que `f` **no disminuye** a lo largo de la ruta. Esto tiene relación con que la heurística de distancia en línea recta de la tabla AIMA es consistente. Al ser consistente, se cumple que el valor de `f` no debería disminuir al avanzar por el camino. Por eso, además de ser admisible, esta heurística funciona muy bien para A* y ayuda a que encuentre el camino de menor costo en este problema.

