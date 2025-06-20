# Módulo 3 – RAG con LangChain y Ollama

Este módulo implementa un sistema de Retrieval-Augmented Generation (RAG) usando LangChain, Ollama y ChromaDB.

## 📁 Estructura

- `data/`: Carpeta donde se colocan los documentos `.txt` que se van a indexar.
- `db/`: Carpeta generada automáticamente con la base vectorial persistente (Chroma).
- `ingest.py`: Lee los documentos, genera embeddings y construye el vector store.
- `main.py`: Ejecuta una consola interactiva donde el usuario puede hacer preguntas usando RAG.

## ▶️ Cómo usar

1. **Ingestar documentos**
   ```bash
   python ingest.py
   ```
   Esto genera los vectores en base a los archivos dentro de `data/`.

2. **Ejecutar chat RAG**
   ```bash
   python main.py
   ```
   Inicia una consola donde podés preguntar en lenguaje natural. Escribí `salir` para terminar.

## 🧠 Tecnologías

- **LangChain** (v0.3.x)
- **Ollama** (`mistral` como LLM, `nomic-embed-text` como embedder)
- **ChromaDB** para almacenamiento vectorial local
- **Python 3.10+**

## ✅ Estado

✔️ Módulo completo y funcional.  
📌 Próximos pasos opcionales:
- Manejo de múltiples usuarios
- Interfaz web o API
- Mejor control de contexto y tokens
