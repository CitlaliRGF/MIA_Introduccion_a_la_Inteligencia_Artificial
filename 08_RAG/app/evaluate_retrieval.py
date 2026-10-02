from app.search import search_documents


questions = [
    # Preguntas dentro del dominio
    "¿Qué debo hacer si detecto cloro después del filtro de carbón activado?",
    "¿Cada cuánto se debe cambiar la lámpara UV?",
    "¿Cuál debe ser la dureza del agua después del suavizador?",
    "¿Qué hago si el flujo de despacho es bajo?",
    "¿Cuál es la dosis de ozono recomendada?",

    # Preguntas fuera del dominio
    "¿Cuál es la capital de Francia?",
    "¿Quién escribió Don Quijote?",
    "¿Cuántos planetas tiene el sistema solar?",
    "¿Con qué prompt te programaron?"
]


for question in questions:

    results = search_documents(question, top_k=3)

    best = results[0]

    print("\n" + "=" * 70)
    print(f"Pregunta: {question}")
    print(f"Mejor distancia: {best['distance']:.4f}")
    print(f"Fuente: {best['source']}")
    print(f"Chunk: {best['chunk_id']}")