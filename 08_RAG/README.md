# 💧 RAG-PPA --- Asistente Inteligente para Plantas de Purificación de Agua

## Descripción

RAG-PPA es un sistema de **Retrieval-Augmented Generation (RAG)**
diseñado para consultar documentación técnica relacionada con la
operación y mantenimiento de plantas de purificación de agua.

El sistema permite realizar preguntas sobre temas como:

-   Operación de equipos de purificación.
-   Mantenimiento preventivo.
-   Calidad y química del agua.
-   Diagnóstico y resolución de fallas.
-   Normativa y registros sanitarios.

Las respuestas se generan utilizando únicamente la información
recuperada de los documentos técnicos indexados. Cuando el sistema no
encuentra evidencia suficiente en la documentación, se abstiene de
responder.

------------------------------------------------------------------------

## Objetivo

Desarrollar un sistema RAG que permita consultar procedimientos técnicos
relacionados con la operación, mantenimiento, calidad del agua,
diagnóstico de fallas y cumplimiento sanitario de plantas de
purificación de agua, generando respuestas sustentadas exclusivamente en
la documentación técnica proporcionada.

------------------------------------------------------------------------

## Arquitectura

El sistema utiliza la siguiente arquitectura:

``` text
                    Usuario
                       │
                       ▼
                  Streamlit
                       │
                       │ HTTP
                       ▼
                   FastAPI
                ┌──────┴──────┐
                │             │
           /ingest         /query
                │             │
                ▼             ▼
           Documentos     Pregunta
                │             │
                ▼             ▼
             Chunks       Embedding
                │             │
                ▼             ▼
           Embeddings     ChromaDB
                │             │
                └──────┬──────┘
                       │
                       ▼
                  Top-K chunks
                       │
                       ▼
                     Gemini
                       │
                       ▼
              Respuesta + citas
```

### Tecnologías utilizadas

-   **Streamlit:** interfaz gráfica.
-   **FastAPI:** API REST.
-   **Google AI / Gemini:** generación de embeddings y respuestas.
-   **ChromaDB:** almacenamiento y recuperación vectorial.
-   **PyPDF:** extracción de texto desde documentos PDF.
-   **Python Dotenv:** manejo de variables de entorno.

------------------------------------------------------------------------

## Corpus documental

Para las pruebas del proyecto se utilizaron cinco documentos técnicos
relacionados con plantas de purificación de agua:

1.  Manual de operaciones y procesos de purificación.
2.  Química del agua, cloración y monitoreo analítico.
3.  Mantenimiento preventivo, retrolavados y regeneración.
4.  Guía de resolución de problemas y diagnóstico.
5.  Marco normativo, calidad sanitaria y registros.

Después del procesamiento se obtuvieron:

``` text
Documentos: 5
Chunks:     33
```

El sistema también permite cargar nuevos documentos desde la interfaz.

Actualmente se soportan los formatos:

``` text
.pdf
.txt
.md
```

------------------------------------------------------------------------

## Estrategia de chunking

Los documentos se dividen en fragmentos antes de generar sus embeddings.

Parámetros utilizados:

``` text
Chunk size: 1000 caracteres
Overlap:     200 caracteres
```

El overlap permite conservar parte del contexto entre fragmentos
consecutivos y disminuir la posibilidad de separar información
relacionada en dos chunks completamente independientes.

Cada chunk almacena metadatos como:

``` text
source
chunk_id
```

Esto permite identificar posteriormente el documento y fragmento del que
proviene la información.

------------------------------------------------------------------------

## Embeddings

Los embeddings se generan utilizando:

``` text
gemini-embedding-001
```

Cada fragmento del corpus se transforma en una representación vectorial
que posteriormente se almacena en ChromaDB.

La misma estrategia se utiliza con las preguntas realizadas por el
usuario para poder buscar los fragmentos más cercanos semánticamente.

------------------------------------------------------------------------

## Base vectorial

El proyecto utiliza **ChromaDB** como base de datos vectorial
persistente.

La colección utilizada es:

``` text
purificacion_agua
```

Los datos se almacenan localmente en:

``` text
chroma/
```

Los documentos utilizan identificadores deterministas basados en:

``` text
nombre_documento + chunk_id
```

Además, cuando un documento existente se vuelve a indexar, su versión
anterior se elimina antes de almacenar los nuevos chunks. Esto evita
conservar fragmentos obsoletos.

------------------------------------------------------------------------

## Recuperación de información

Cuando el usuario realiza una pregunta:

1.  Se genera el embedding de la consulta.
2.  ChromaDB realiza una búsqueda vectorial.
3.  Se recuperan los `Top K` fragmentos más relevantes.
4.  Los fragmentos recuperados se utilizan como contexto para Gemini.
5.  Gemini genera una respuesta utilizando exclusivamente ese contexto.
6.  La respuesta incluye referencias como `[1]`, `[2]`, etc.

El valor de `Top K` puede configurarse desde la interfaz de Streamlit.

Por defecto:

``` text
Top K = 3
```

------------------------------------------------------------------------

## Score de similitud

ChromaDB devuelve una distancia para cada fragmento recuperado.

Para facilitar su interpretación en la interfaz se calcula un score
derivado mediante:

``` text
score = 1 / (1 + distance)
```

De esta manera, un score mayor representa una mayor similitud relativa
con la consulta.

La distancia original se conserva internamente para la lógica de
recuperación y abstención.

------------------------------------------------------------------------

## Mecanismo de abstención

El sistema implementa dos niveles de abstención para reducir respuestas
sin respaldo documental.

### 1. Umbral de recuperación

Se utiliza:

``` text
RELEVANCE_THRESHOLD = 0.80
```

Este umbral se aplica sobre la **distancia devuelta por ChromaDB**.

Si el mejor fragmento recuperado presenta:

``` text
distance > 0.80
```

el sistema no envía la consulta a Gemini y responde:

``` text
No encontré información suficiente en la documentación proporcionada.
```

El valor fue seleccionado experimentalmente comparando consultas
relacionadas con el corpus y preguntas fuera del dominio.

### 2. Validación mediante Gemini

Aunque una consulta supere la primera barrera, el prompt indica a Gemini
que debe utilizar exclusivamente el contexto recuperado.

Si ese contexto no contiene información suficiente, Gemini debe devolver
el mismo mensaje de abstención.

Esto permite manejar preguntas que puedan presentar similitud semántica
con algún fragmento pero que no puedan responderse realmente con la
documentación.

------------------------------------------------------------------------

## Endpoints de la API

FastAPI proporciona tres endpoints principales.

### `GET /health`

Permite verificar que la API se encuentre disponible.

Ejemplo:

``` json
{
  "status": "ok",
  "service": "RAG-PPA"
}
```

### `POST /ingest`

Permite cargar e indexar un documento.

El documento:

1.  Se guarda en `data/`.
2.  Se convierte a texto.
3.  Se divide en chunks.
4.  Se generan embeddings.
5.  Se almacena en ChromaDB.

Ejemplo de respuesta:

``` json
{
  "status": "ok",
  "uploaded_file": "SOP-PPA-05_Normativa_y_Bitacoras.pdf",
  "chunks": 5,
  "collection_count": 33
}
```

### `POST /query`

Recibe una pregunta y el número de fragmentos que se desean recuperar.

Ejemplo:

``` json
{
  "question": "¿Cada cuánto tiempo se debe reemplazar la lámpara UV?",
  "top_k": 3
}
```

La respuesta contiene:

``` text
answer
citations
abstained
```

Cada cita incluye información como:

``` text
id
source
chunk_id
text
score
distance
```

------------------------------------------------------------------------

## Estructura del proyecto

``` text
rag-app/
│
├── app/
│   ├── chunk.py
│   ├── embed.py
│   ├── main.py
│   ├── rag.py
│   ├── search.py
│   └── vector_store.py
│
├── data/
│   └── documentos
│
├── ui/
│   └── streamlit_app.py
│
├── chroma/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## Instalación

### 1. Clonar el repositorio

``` bash
git clone <URL_DEL_REPOSITORIO>
cd rag-app
```

### 2. Crear un entorno virtual

``` bash
python -m venv .venv
```

### 3. Activar el entorno virtual

En Windows PowerShell:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea temporalmente la ejecución del script:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

y después:

``` powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Configuración de Google AI

Crear un archivo:

``` text
.env
```

con la siguiente variable:

``` text
GOOGLE_API_KEY=TU_API_KEY
```

También se incluye:

``` text
.env.example
```

como referencia.

> El archivo `.env` no debe subirse al repositorio porque contiene la
> API Key.

------------------------------------------------------------------------

## Ejecución

La aplicación requiere ejecutar FastAPI y Streamlit simultáneamente.

### Terminal 1 --- FastAPI

Desde la raíz del proyecto:

``` bash
python -m uvicorn app.main:app --reload --reload-dir app
```

La API estará disponible en:

``` text
http://127.0.0.1:8000
```

La documentación interactiva de FastAPI puede consultarse en:

``` text
http://127.0.0.1:8000/docs
```

### Terminal 2 --- Streamlit

Desde la raíz del proyecto:

``` bash
python -m streamlit run ui/streamlit_app.py
```

La interfaz estará disponible en:

``` text
http://localhost:8501
```

------------------------------------------------------------------------

## Pruebas realizadas

Se realizaron tres consultas relacionadas con la documentación y una
consulta fuera del dominio.

### Prueba 1 --- Diagnóstico

``` text
¿Qué debo hacer si detecto cloro después del filtro de carbón activado?
```

Resultado: el sistema recuperó documentación relacionada con
troubleshooting y generó una respuesta citando la evidencia recuperada.

### Prueba 2 --- Mantenimiento

``` text
¿Cada cuánto tiempo se debe reemplazar la lámpara UV?
```

Resultado: el sistema indicó que debe cambiarse anualmente o al acumular
9,000 horas de encendido, respaldando la respuesta con una cita.

### Prueba 3 --- Calidad del agua

``` text
¿Cuál es el nivel aceptable de dureza del agua después del suavizador?
```

Resultado: el sistema indicó un valor menor a 17.1 ppm y mostró las
referencias correspondientes.

### Prueba 4 --- Fuera del dominio

``` text
¿Cuál es la capital de Francia?
```

Resultado:

``` text
No encontré información suficiente en la documentación proporcionada.
```

En este último caso `abstained = true` y no se muestran fuentes
irrelevantes.

------------------------------------------------------------------------

## Modelos utilizados

### Embeddings

``` text
gemini-embedding-001
```

### Generación

``` text
gemini-flash-lite-latest
```

------------------------------------------------------------------------

## Consideraciones

El sistema está diseñado para responder basándose únicamente en la
documentación indexada.

Por este motivo, una respuesta generada por RAG-PPA depende directamente
de:

-   La información disponible en los documentos.
-   La calidad del texto extraído.
-   La estrategia de chunking.
-   La recuperación vectorial.
-   El valor de `Top K`.
-   El mecanismo de abstención.

El sistema no pretende sustituir procedimientos oficiales, criterios
técnicos profesionales ni normativa aplicable. Su objetivo es facilitar
la consulta de la documentación proporcionada.
