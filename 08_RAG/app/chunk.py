from pathlib import Path

from pypdf import PdfReader


DATA_DIR = Path("data")

# Formatos que actualmente soporta el sistema
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def read_pdf(file_path: Path) -> str:
    """
    Extrae texto de un archivo PDF.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_text_file(file_path: Path) -> str:
    """
    Lee archivos de texto plano o Markdown.
    """

    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def read_document(file_path: Path) -> str:
    """
    Detecta el tipo de archivo y utiliza
    el lector correspondiente.
    """

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    if extension in {".txt", ".md"}:
        return read_text_file(file_path)

    raise ValueError(
        f"Formato no soportado: {extension}"
    )


def create_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Divide un texto en fragmentos con solapamiento.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents() -> list[dict]:
    """
    Lee todos los documentos compatibles de data/
    y devuelve sus chunks junto con sus metadatos.
    """

    documents = []

    files = sorted(
        file_path
        for file_path in DATA_DIR.iterdir()
        if (
            file_path.is_file()
            and file_path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    )

    for file_path in files:

        print(f"Leyendo: {file_path.name}")

        text = read_document(file_path)

        chunks = create_chunks(text)

        for index, chunk in enumerate(chunks):

            documents.append(
                {
                    "text": chunk,
                    "source": file_path.name,
                    "chunk_id": index
                }
            )

        print(f"  → {len(chunks)} chunks")

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print("\n-----------------------------")
    print(f"TOTAL DE CHUNKS: {len(documents)}")
    print("-----------------------------")

    if documents:

        print("\nEJEMPLO DEL PRIMER CHUNK:\n")

        print(
            f"Fuente: {documents[0]['source']}"
        )

        print(
            f"Chunk: {documents[0]['chunk_id']}"
        )

        print()

        print(
            documents[0]["text"]
        )