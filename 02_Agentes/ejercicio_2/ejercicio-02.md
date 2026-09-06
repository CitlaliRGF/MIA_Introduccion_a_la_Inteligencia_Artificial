# Ejercicio 2 — Descripción PEAS de agentes inteligentes


### 1. Asistente virtual de voz

- **Performance:** Interpreta correctamente a lo que se le pregunta, el tiempo de espera de la respuesta, también seria bueno contemplar el porcentaje de comandos que siguió correctamente. 
- **Environment:** Dentro de una casa, un negocio, oficina. Es parcialmente observable, estocástico, secuencial y dinámico, porque el agente no sabe todo lo que ocurre.
- **Actuators:** Reproduce música, llamada telefónica, encender o apagar un dispositivo.
- **Sensors:** Micrófono, calendario, información proveniente de internet, estado del clima.


### 2. Robot aspirador doméstico

- **Performance:** Mapeo correcto del lugar de aspirado, consumo de batería, el tiempo de limpieza, reconocimiento de objetos, humanos, mascotas.
- **Environment:** Casa o departamento. Es parcialmente observable, estocástico, secuencial y dinámico, porque las personas, masconas o incluso muebles pueden cambiar de lugar.
- **Actuators:** Cepillos, llantas o bandas de movimiento, motor para aspirar.
- **Sensors:** Sensores de proximidad o movimiento, detectores de suciedad.


### 3. Sistema de recomendación de streaming

- **Performance:** Recomienda contenido de acorde al gusto del usuario, proporción de recomendaciones seguidas y no seguidas por el usuario.
- **Environment:** Plataformas de reproducción. Es parcialmente observable, estocástico, secuencial y dinámico, porque el sistema no conoce al 100% al usuario y muchas veces la elección de contenido de las personas puede cambiar de acuerdo a comportamientos.
- **Actuators:** Reproducir música recomendada, reproducir una película, crear listas para ver7escuchar después de cierto contenido.
- **Sensors:** El historial de películas o música vistas/escuchadas, tráiler vistos por un tiempo considerable recientemente, búsquedas, agregados recientemente, likes.


### 4. Vehículo autónomo en ciudad

- **Performance:** Llegar al lugar correcto, respetar los señalamientos/semáforos, conducir de manera segura.
- **Environment:** Calles o carretera, clima, pasajeros, otros automóviles. Al igual que los ejemplos anteriores, considero que es parcialmente observable, estocástico, secuencial y dinámico, porque inicialmente el auto no conoce a la perfección de otros coches/personas ya que estos pueden cambiar de un momento para otro.
- **Actuators:** Girar el volante, acelerar o frenar el auto, encender apagar luces.
- **Sensors:** GPS, micrófono, sensores de movimiento, sensores de proximidad, cámaras.


### 5. Agente de trading algorítmico en bolsa

- **Performance:** Costos de acciones, ganancias obtenidas, perdida obtenida, rendimiento de inversión.
- **Environment:** Mercados financieros. Es parcialmente observable, estocástico, secuencial y dinámico porque los precios en el mercado cambian a cada rato.
- **Actuators:** Comprar/vender acciones.
- **Sensors:** Historial de precios del mercado, noticias del sector financiero o incluso político, saldo disponible, KPIs económicos.


### 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** Diagnostico correcto, tiempo de análisis de síntomas, seguridad de los resultados.
- **Environment:** Consultorio Medico, Sistema de medicina online con médicos, hospitales. Es parcialmente observable, estocástico, secuencial y dinámico porque no sabe toda la información del paciente más allá de lo que comenta y en temas de salud las condiciones pueden cambiar de forma inesperada.
- **Actuators:** Hacer el reporte médico, sugerir un diagnostico.
- **Sensors:** Análisis sanguíneos, historiales de pacientes, analizar imágenes de radiografías, resonancias, etc.


### 7. Dron de inspección de infraestructura 

- **Performance:** Tiempo de vuelo, identifica y clasifica de forma adecuada cables pelados, estructuras de metal oxidadas, advierte de posibles fugas de agua, gas, etc. 
- **Environment:** Obras en construcción, edificios, instalaciones industriales y domesticas, líneas eléctricas. Es parcialmente observable, estocástico, secuencial, dinámico y continuo, porque el dron se ve afectado por las condiciones ambientales.
- **Actuators:** Hélices, rotores, motores.
- **Sensors:** Sensores ópticos y térmicos, sensores de proximidad, sensores inerciales, GPS, cámara.


### 8. Agente jugador de ajedrez  

- **Performance:** Ganar una partida, moverse de forma correcta respetando las reglas, eficiencia con la que usa su tiempo disponible.
- **Environment:**  Tablero de juego, oponente. Es totalmente observable, determinista, secuencial, dinámico y discreto, porque se conoce todo el tablero de juego y cada movimiento modifica el estado del mismo.
- **Actuators:** Mover piezas, capturar piezas, abandonar la partida.
- **Sensors:**  Cronometro, historial de jugadas o movimientos.




