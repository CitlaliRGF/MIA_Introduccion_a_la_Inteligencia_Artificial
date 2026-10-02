import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

st.set_page_config(
    page_title="RAG-PPA",
    page_icon="💧",
    layout="centered"
)


# ---------------------------------------------------------
# Encabezado
# ---------------------------------------------------------

st.title("💧 RAG-PPA")

st.subheader(
    "Asistente para Plantas de Purificación de Agua"
)

st.write(
    "Consulta procedimientos de operación, mantenimiento, "
    "calidad del agua y diagnóstico de fallas."
)


# ---------------------------------------------------------
# Carga e indexación de documentos
# ---------------------------------------------------------

st.markdown("## 📚 Documentos")

uploaded_file = st.file_uploader(
    "Selecciona un documento",
    type=["pdf", "txt", "md"]
)

if uploaded_file is not None:

    if st.button(
        "Indexar documento",
        type="secondary"
    ):

        try:

            with st.spinner(
                "Procesando e indexando documento..."
            ):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/ingest",
                    files=files,
                    timeout=180
                )

                response.raise_for_status()

                data = response.json()

            if data["status"] == "ok":

                st.success(
                    "Documento indexado correctamente."
                )

                st.write(
                    f"**Archivo:** "
                    f"{data['uploaded_file']}"
                )

                st.write(
                    f"**Chunks generados:** "
                    f"{data['chunks']}"
                )

                st.write(
                    f"**Registros en ChromaDB:** "
                    f"{data['collection_count']}"
                )

            else:

                st.error(
                    data.get(
                        "message",
                        "No fue posible indexar el documento."
                    )
                )

        except requests.exceptions.RequestException:

            st.error(
                "No fue posible conectarse con la API. "
                "Verifica que FastAPI esté ejecutándose."
            )


st.divider()


# ---------------------------------------------------------
# Consulta RAG
# ---------------------------------------------------------

st.markdown("## 💬 Consulta")

question = st.text_area(
    "Escribe tu pregunta:",
    placeholder=(
        "Ejemplo: ¿Qué debo hacer si detecto cloro "
        "después del filtro de carbón activado?"
    )
)

top_k = st.slider(
    "Número de fragmentos a recuperar (Top K)",
    min_value=1,
    max_value=10,
    value=3
)


if st.button(
    "Consultar",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Escribe una pregunta antes de consultar."
        )

    else:

        try:

            with st.spinner(
                "Consultando documentación..."
            ):

                response = requests.post(
                    f"{API_URL}/query",
                    json={
                        "question": question,
                        "top_k": top_k
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

            # -------------------------------------------------
            # Respuesta
            # -------------------------------------------------

            st.markdown("### Respuesta")

            st.markdown(
                data["answer"]
            )

            # -------------------------------------------------
            # Abstención
            # -------------------------------------------------

            if data["abstained"]:

                st.info(
                    "El sistema se abstuvo de responder "
                    "porque no encontró evidencia suficiente "
                    "en la documentación."
                )

            # -------------------------------------------------
            # Citas
            # -------------------------------------------------

            elif data["citations"]:

                st.markdown(
                    "### 📖 Fuentes utilizadas"
                )

                for citation in data["citations"]:

                    title = (
                        f"[{citation['id']}] "
                        f"{citation['source']} "
                        f"— Chunk {citation['chunk_id']} "
                        f"— Score "
                        f"{citation['score']:.4f}"
                    )

                    with st.expander(title):

                        st.write(
                            citation["text"]
                        )

        except requests.exceptions.RequestException:

            st.error(
                "No fue posible conectarse con la API. "
                "Verifica que FastAPI esté ejecutándose."
            )