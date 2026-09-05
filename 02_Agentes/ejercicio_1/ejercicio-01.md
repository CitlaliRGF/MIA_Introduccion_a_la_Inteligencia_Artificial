# Ejercicio 01 — Cambiar la ubicación del Wumpus y los pits

## 1\. Configuración de la cueva

Para este ejercicio se creó el archivo:

`Agentes/project/config/mi_cueva_4x4.yaml`

La configuración utilizada fue:

```yaml
grid:
  width: 4
  height: 4

agent:
  start: [1, 1]
  direction: east
  arrows: 1

wumpus: [3, 3]

pits:
  - [4, 1]
  - [4, 3]
  - [2, 4]

gold: \[3, 2]

scoring:
  gold: 1000
  death: -1000
  step: -1
  shoot: -10

max_steps: 200
```

## 2\. Diagrama de la cueva

Las coordenadas tienen origen en `\[1,1]`, ubicada en la esquina inferior izquierda.

```text
        1   2   3   4
     ┌───┬───┬───┬───┐
  4  │ · │ P │ · │ · │
     ├───┼───┼───┼───┤
  3  │ · │ · │ W │ P │
     ├───┼───┼───┼───┤
  2  │ · │ · │ G │ · │
     ├───┼───┼───┼───┤
  1  │ → │ · │ · │ P │
     └───┴───┴───┴───┘
        1   2   3   4

→ Agente
W Wumpus
P Pit
G Gold
· Casilla vacía


## 3\. Resultados de los agentes

Los agentes se ejecutaron utilizando la misma configuración de la cueva.

|Agente|Resultado|Pasos|Score|
|-|-|-:|-:|
|Simple Reflex|No obtuvo el oro|200|-200|
|Model-Based|Obtuvo el oro|17|983|
|Goal-Based|Obtuvo el oro|17|983|
|Utility-Based|Obtuvo el oro|34|956|
|Learning|Obtuvo el oro|12|988|

El Learning Agent fue entrenado durante 1500 episodios. En la ejecución greedy (`epsilon = 0`) obtuvo el oro en 12 pasos, con un score de 988.

## 

## 4\. Reporte

Los agentes Model-Based, Goal-Based, Utility-Based y Learning lograron obtener el oro.

El agente Simple Reflex no logró obtenerlo. Alcanzó el límite de 200 pasos y terminó con un score de -200.

La diferencia principal está en la cantidad de información que cada agente utiliza para tomar decisiones. El agente Simple Reflex solamente reacciona a la percepción actual, mientras que los otros agentes utilizan memoria, objetivos, utilidad o aprendizaje para tomar decisiones más elaboradas. El agente Simple Reflex toma decisiones únicamente a partir de la percepción que recibe en el momento. No mantiene una representación del mapa ni recuerda las casillas que ya visitó.

En esta configuración, el pit ubicado en `\[4,1]` provoca una brisa en `\[3,1]`. Cuando el agente llega a `\[3,1]`, detecta la brisa y aplica su regla reactiva para girar. Como no tiene memoria ni capacidad para planificar una ruta alternativa, puede comenzar a repetir movimientos y quedar atrapado en un ciclo.

Por eso este agente puede fallar aunque exista una ruta segura hacia el oro. Su comportamiento depende de las percepciones inmediatas y, en algunos mapas, podría tener suerte y encontrar el oro.

La posición de los pits modifica las percepciones que recibe el agente y, por lo tanto, la información que puede utilizar para determinar qué casillas son seguras.

Si un pit se mueve más cerca del inicio, es más probable que el agente perciba una brisa en las primeras casillas. Para un agente Model-Based esto puede reducir las casillas que considera seguras y dificultar la exploración. En algunos casos puede detenerse porque no encuentra una ruta que pueda considerar segura.

Si el pit se mueve más lejos del inicio, el agente puede avanzar varias casillas obteniendo percepciones sin brisa. Estas observaciones le permiten ampliar su conocimiento sobre las casillas seguras y pueden facilitar la búsqueda de una ruta hacia el oro.

Por lo tanto, la ubicación de los pits no solo cambia el peligro físico del mapa, sino también la información disponible para los agentes que construyen un modelo del entorno.





En conclusión, el experimento muestra que agregar memoria, objetivos, evaluación de utilidad o aprendizaje permite que los agentes tengan un comportamiento más robusto que un agente puramente reactivo.



