# ─── IMPORTS NUEVOS (sin deprecations) ─────────────────────────────────────────
from langchain_chroma import Chroma  # nuevo vectorstore
from langchain_ollama import OllamaEmbeddings, OllamaLLM  # embeddings y LLM
from langchain.chains import RetrievalQA

CHROMA_PATH = "db"  # carpeta con la BD

# 1️⃣ Embeddings correctos
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2️⃣ Cargamos la base Chroma
vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)

# 3️⃣ LLM local (Mistral)
llm = OllamaLLM(model="mistral")

# 4️⃣ Cadena RAG: retrieval + generación
qa = RetrievalQA.from_chain_type(
    llm=llm, retriever=vectordb.as_retriever(), chain_type="stuff"
)

print("\n💬 RAG activo — escribí 'salir' para terminar.\n")

while True:
    pregunta = input("🧑 Tú: ")
    if pregunta.lower() in {"salir", "exit", "quit"}:
        print("👋 ¡Hasta luego!")
        break

    respuesta = qa.invoke(pregunta)  # invoke es la nueva forma recomendada
    texto = respuesta["result"] if isinstance(respuesta, dict) else respuesta
    print(f"🤖 Mistral: {texto}\n")
