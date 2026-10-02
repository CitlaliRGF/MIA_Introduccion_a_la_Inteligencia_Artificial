from app.embed import create_embedding
from app.vector_store import get_collection


def search_documents(query: str, top_k: int = 3) -> list[dict]:
    """Busca los chunks más similares a una pregunta."""

    collection = get_collection()

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = []

    for i in range(len(results["documents"][0])):

        documents.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "chunk_id": results["metadatas"][0][i]["chunk_id"],
                "distance": results["distances"][0][i],
                "score": 1 / (
                    1 + results["distances"][0][i]
                    )
            }
        )

    return documents


if __name__ == "__main__":

    question = (
        "¿Qué debo hacer si detecto cloro "
        "después del filtro de carbón activado?"
    )

    print("\nPREGUNTA:")
    print(question)

    results = search_documents(question)

    print("\nRESULTADOS:")

    for i, result in enumerate(results, start=1):

        print("\n" + "=" * 70)
        print(f"RESULTADO {i}")
        print(f"Fuente: {result['source']}")
        print(f"Chunk: {result['chunk_id']}")
        print(f"Distancia: {result['distance']:.4f}")
        print("-" * 70)
        print(result["text"])