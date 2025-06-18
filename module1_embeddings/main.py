from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document


def main():
    """Ejemplo mínimo de buscador semántico con ChromaDB + LangChain."""

    # 1️⃣ Modelo de embeddings local (sentence‑transformers)
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # 🧬 Mostrar un embedding de ejemplo
    vec = embedding_model.embed_query("Estoy aprendiendo inteligencia artificial")
    print(f"\n🧬 Embedding (primeros 10 valores): {vec[:10]}")
    print(f"🔢 Dimensión: {len(vec)}")  # 384

    # 2️⃣ Documentos a indexar (en producción los cargarás desde archivos)
    docs = [
        Document(page_content="Estoy aprendiendo inteligencia artificial"),
        Document(page_content="El perro duerme todo el día"),
        Document(page_content="Hoy hace calor en Buenos Aires"),
    ]

    # 3️⃣ Crear/cargar la base Chroma persistente
    db = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory="./chroma_db_mpnet",  # nuevo folder
        collection_metadata={"hnsw:space": "cosine"},
    )

    # 4️⃣ Consulta semántica
    query = "Estoy estudiando IA"
    results = db.similarity_search_with_relevance_scores(query, k=3)

    print("\n🔎 Resultados con score (1.0 = idéntico):")
    for doc, score in results:
        print(f"{score:.3f} → {doc.page_content}")


if __name__ == "__main__":
    main()
