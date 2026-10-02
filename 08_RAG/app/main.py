from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field

from app.chunk import SUPPORTED_EXTENSIONS
from app.rag import ask_rag
from app.vector_store import index_document


app = FastAPI(
    title="RAG-PPA API",
    description="Asistente RAG para plantas de purificación de agua",
    version="1.0.0"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Modelos de entrada
# ---------------------------------------------------------

class QueryRequest(BaseModel):
    question: str
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Número de chunks a recuperar"
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "RAG-PPA"
    }


# ---------------------------------------------------------
# Indexación de documentos
# ---------------------------------------------------------

@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...)
):
    """
    Recibe un documento compatible, lo guarda en data/
    y lo indexa en ChromaDB.
    """

    # Obtener extensión
    extension = Path(file.filename).suffix.lower()

    # Validar formato
    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "status": "error",
            "message": (
                "Formato no soportado. "
                "Formatos permitidos: PDF, TXT y MD."
            )
        }

    # Usamos solamente el nombre del archivo.
    # Evita que una ruta enviada como nombre salga de data/.
    safe_filename = Path(file.filename).name

    file_path = DATA_DIR / safe_filename

    # Guardar archivo
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Indexar solamente el documento recibido
    try:
        result = index_document(file_path)

    except Exception as e:
        return {
            "status": "error",
            "message": f"No fue posible indexar el documento: {str(e)}"
        }

    return {
        "status": result["status"],
        "uploaded_file": safe_filename,
        "chunks": result["chunks"],
        "collection_count": result["collection_count"]
    }


# ---------------------------------------------------------
# Consulta RAG
# ---------------------------------------------------------

@app.post("/query")
def query(request: QueryRequest):

    result = ask_rag(
        question=request.question,
        top_k=request.top_k
    )

    return {
        "answer": result["answer"],
        "citations": result["citations"],
        "abstained": result["abstained"]
    }