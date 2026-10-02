import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "No se encontró GOOGLE_API_KEY. "
        "Verifica que exista en el archivo .env."
    )

client = genai.Client(api_key=api_key)


def create_embedding(text: str) -> list[float]:
    """Convierte un texto en un vector usando Google AI."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


if __name__ == "__main__":

    test_text = (
        "El filtro de carbón activado elimina cloro "
        "y compuestos orgánicos del agua."
    )

    embedding = create_embedding(test_text)

    print("Texto:")
    print(test_text)

    print("\nPrimeros 10 valores del embedding:")
    print(embedding[:10])

    print("\nDimensión del vector:")
    print(len(embedding))