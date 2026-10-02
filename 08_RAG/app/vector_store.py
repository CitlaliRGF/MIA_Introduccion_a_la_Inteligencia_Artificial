from pathlib import Path

import chromadb

from app.chunk import (
    load_documents,
    read_document,
    create_chunks
)
from app.embed import create_embedding


CHROMA_DIR = Path("chroma")
COLLECTION_NAME = "purificacion_agua"


def get_collection():
    """
    Obtiene o crea la colección persistente de ChromaDB.
    """

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def index_document(file_path: Path) -> dict:
    """
    Procesa e indexa un único documento compatible.
    """

    collection = get_collection()

    # ---------------------------------------------------------
    # 1. Leer el documento
    # ---------------------------------------------------------
    text = read_document(file_path)

    if not text.strip():
        return {
            "status": "error",
            "source": file_path.name,
            "chunks": 0,
            "collection_count": collection.count(),
            "message": "No se pudo extraer texto del documento."
        }

    # ---------------------------------------------------------
    # 2. Crear chunks
    # ---------------------------------------------------------
    chunks = create_chunks(text)

    print(f"\nIndexando: {file_path.name}")
    print(f"Chunks encontrados: {len(chunks)}")

    # ---------------------------------------------------------
    # 3. Eliminar la versión anterior del mismo documento
    # ---------------------------------------------------------
    collection.delete(
        where={"source": file_path.name}
    )

    # ---------------------------------------------------------
    # 4. Crear embeddings e indexar los chunks
    # ---------------------------------------------------------
    for index, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        document_id = (
            f"{file_path.name}_chunk_{index}"
        )

        collection.upsert(
            ids=[document_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": file_path.name,
                    "chunk_id": index
                }
            ]
        )

        print(
            f"[{index + 1}/{len(chunks)}] "
            f"{file_path.name} - chunk {index}"
        )

    collection_count = collection.count()

    print("\nDocumento indexado correctamente.")
    print(f"Chunks indexados: {len(chunks)}")
    print(
        f"Registros totales en ChromaDB: "
        f"{collection_count}"
    )

    return {
        "status": "ok",
        "source": file_path.name,
        "chunks": len(chunks),
        "collection_count": collection_count
    }


def index_documents() -> dict:
    """
    Indexa todos los documentos compatibles disponibles en data/.
    """

    documents = load_documents()

    if not documents:
        return {
            "status": "empty",
            "documents": 0,
            "chunks": 0,
            "collection_count": 0
        }

    collection = get_collection()

    unique_sources = {
        document["source"]
        for document in documents
    }

    print("\nGenerando embeddings...")

    for i, document in enumerate(documents):

        embedding = create_embedding(
            document["text"]
        )

        document_id = (
            f"{document['source']}_"
            f"chunk_{document['chunk_id']}"
        )

        collection.upsert(
            ids=[document_id],
            documents=[document["text"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": document["source"],
                    "chunk_id": document["chunk_id"]
                }
            ]
        )

        print(
            f"[{i + 1}/{len(documents)}] "
            f"{document['source']} "
            f"- chunk {document['chunk_id']}"
        )

    collection_count = collection.count()

    print("\nIndexación terminada.")
    print(
        f"Documentos procesados: "
        f"{len(unique_sources)}"
    )
    print(
        f"Chunks procesados: "
        f"{len(documents)}"
    )
    print(
        f"Registros en ChromaDB: "
        f"{collection_count}"
    )

    return {
        "status": "ok",
        "documents": len(unique_sources),
        "chunks": len(documents),
        "collection_count": collection_count
    }


if __name__ == "__main__":

    result = index_documents()

    print("\nRESULTADO:")
    print(result)