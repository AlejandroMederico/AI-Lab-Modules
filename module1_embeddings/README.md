# 🧠 Módulo 1 — Embeddings y Búsqueda Semántica con ChromaDB

Este módulo es parte de un proyecto educativo práctico sobre inteligencia artificial aplicado a búsqueda semántica, RAG y agentes inteligentes. Acá trabajamos desde cero con herramientas 100% locales y gratuitas.

---

## ✅ Objetivo

Aprender a generar **embeddings de texto** y realizar **búsquedas semánticas** usando:

- `sentence-transformers` (modelo local)
- `ChromaDB` como base vectorial persistente
- `LangChain` para orquestar el flujo

---

## 🧩 Tecnologías utilizadas

| Herramienta              | Rol                                      |
|--------------------------|-------------------------------------------|
| `sentence-transformers` | Generar vectores (embeddings)             |
| `langchain`             | Orquestación de flujos                    |
| `chroma`                | Base de datos vectorial persistente       |
| `langchain-community`   | Módulo donde viven los vectorstores       |
| `langchain-huggingface` | Módulo para usar modelos HF con LangChain |

---

## 📦 Instalación

```bash
python -m venv env
source env/bin/activate   # o env\Scripts\activate en Windows
pip install -r requirements.txt
```

---

## 🚀 Uso

```bash
python main.py
```

Este script:
1. Genera un embedding local de ejemplo
2. Indexa documentos en ChromaDB
3. Ejecuta una búsqueda semántica con scores de similitud

---

## 🔎 Resultado esperado (ejemplo)

```text
🔎 Resultados con score (1.0 = idéntico):
0.571 → Estoy aprendiendo inteligencia artificial
0.503 → Hoy hace calor en Buenos Aires
0.447 → El perro duerme todo el día
```

---

## 📂 Estructura del proyecto

```
module1_embeddings/
├── main.py               # Script principal
├── requirements.txt      # Librerías necesarias
├── README.md             # Documentación (este archivo)
└── chroma_db_mpnet/      # Persistencia automática de Chroma
```

---

## 🧠 Lo aprendido en este módulo

- Qué es un embedding y cómo generarlo localmente
- Cómo usar ChromaDB como vector store local persistente
- Qué es la similitud coseno y cómo interpretarla
- Cómo comparar modelos (MiniLM vs MPNet)

---

## ⏭️ Próximo módulo

**Módulo 2: Modelos de lenguaje (LLMs)**
> Cómo usar Ollama o APIs para generar respuestas, interactuar con texto y conectar todo con RAG.

---

## 💡 Autor

Creado por Alejandro como parte de un curso práctico personal de IA. Proyecto en evolución.
