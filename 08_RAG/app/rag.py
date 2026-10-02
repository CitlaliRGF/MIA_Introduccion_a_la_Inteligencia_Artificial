from google import genai

from app.embed import api_key
from app.search import search_documents


# Cliente de Google Gemini
client = genai.Client(api_key=api_key)

# Umbral definido a partir de nuestras pruebas de recuperación.
# Una distancia menor indica mayor cercanía con la consulta.
RELEVANCE_THRESHOLD = 0.80

# Mensaje estándar de abstención
ABSTENTION_MESSAGE = (
    "No encontré información suficiente "
    "en la documentación proporcionada."
)


def ask_rag(question: str, top_k: int = 3) -> dict:
    """
    Responde una pregunta utilizando exclusivamente
    la información recuperada de la documentación.
    """

    # ---------------------------------------------------------
    # 1. Recuperar los chunks más relevantes desde ChromaDB
    # ---------------------------------------------------------
    results = search_documents(
        query=question,
        top_k=top_k
    )

    # Si por alguna razón no existen resultados
    if not results:
        return {
            "question": question,
            "answer": ABSTENTION_MESSAGE,
            "citations": [],
            "abstained": True,
            "retrieved_chunks": []
        }

    # ---------------------------------------------------------
    # 2. Construir las citas a partir de los chunks recuperados
    # ---------------------------------------------------------
    citations = []

    for i, result in enumerate(results, start=1):
        citations.append(
            {
                "id": i,
                "source": result["source"],
                "chunk_id": result["chunk_id"],
                "text": result["text"],
                "score": result["score"],
                "distance": result["distance"]
            }
        )

    # ---------------------------------------------------------
    # 3. Primera barrera de abstención:
    #    validar la distancia del mejor resultado
    # ---------------------------------------------------------
    best_distance = results[0]["distance"]

    if best_distance > RELEVANCE_THRESHOLD:
        return {
            "question": question,
            "answer": ABSTENTION_MESSAGE,
            "citations": [],
            "abstained": True,
            "retrieved_chunks": results
        }

    # ---------------------------------------------------------
    # 4. Construir el contexto que recibirá Gemini
    # ---------------------------------------------------------
    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"""
FUENTE [{i}]
Documento: {result["source"]}
Chunk: {result["chunk_id"]}

{result["text"]}
"""
        )

    context = "\n".join(context_parts)

    # ---------------------------------------------------------
    # 5. Prompt para generación aumentada por recuperación
    # ---------------------------------------------------------
    prompt = f"""
Eres un asistente técnico especializado en operación y mantenimiento
de plantas de purificación de agua.

Debes responder utilizando EXCLUSIVAMENTE la información proporcionada
en el CONTEXTO.

Reglas:
1. No utilices conocimientos externos.
2. No inventes información.
3. Si el contexto no contiene información suficiente para responder,
   responde exactamente:
   "{ABSTENTION_MESSAGE}"
4. Responde de manera clara y concisa.
5. Cita la evidencia dentro de la respuesta utilizando [1], [2], [3],
   etc., según el número de FUENTE proporcionado en el contexto.
6. No incluyas una sección de fuentes al final de la respuesta.
   La aplicación mostrará las fuentes por separado.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
"""

    # ---------------------------------------------------------
    # 6. Generar la respuesta con Gemini
    # ---------------------------------------------------------
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    answer = response.text.strip()

    # ---------------------------------------------------------
    # 7. Segunda barrera de abstención:
    #    Gemini determina que el contexto no es suficiente
    # ---------------------------------------------------------
    if answer == ABSTENTION_MESSAGE:
        return {
            "question": question,
            "answer": ABSTENTION_MESSAGE,
            "citations": [],
            "abstained": True,
            "retrieved_chunks": results
        }

    # ---------------------------------------------------------
    # 8. Respuesta final
    # ---------------------------------------------------------
    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "abstained": False,
        "retrieved_chunks": results
    }


# -------------------------------------------------------------
# Prueba local
# -------------------------------------------------------------
if __name__ == "__main__":

    question = (
        "¿Qué debo hacer si detecto cloro "
        "después del filtro de carbón activado?"
    )

    result = ask_rag(
        question=question,
        top_k=3
    )

    print("\nPREGUNTA:")
    print(result["question"])

    print("\nRESPUESTA:")
    print(result["answer"])

    print("\nABSTENCIÓN:")
    print(result["abstained"])

    print("\nCITAS:")

    if result["citations"]:
        for citation in result["citations"]:
            print(
                f"[{citation['id']}] "
                f"{citation['source']} "
                f"(chunk {citation['chunk_id']}) "
                f"- distancia: {citation['distance']:.4f}"
            )
    else:
        print("Sin citas.")