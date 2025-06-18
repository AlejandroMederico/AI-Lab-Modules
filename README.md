# 🧠 AI Lab Modules — Curso práctico de inteligencia artificial aplicada

Este repositorio contiene una serie de módulos prácticos enfocados en aprender e implementar componentes reales de inteligencia artificial, búsqueda semántica y agentes inteligentes. Todo está construido con herramientas open source y pensado para correr **localmente**, sin depender de servicios pagos.

---

## 📚 Módulos disponibles

| Módulo | Tema                                               | Estado    |
|--------|----------------------------------------------------|-----------|
| 1️⃣     | Embeddings + Búsqueda semántica con ChromaDB      | ✅ Listo   |
| 2️⃣     | Modelos de lenguaje (LLMs) con Ollama / API       | 🔜 En curso|
| 3️⃣     | RAG: Retrieval-Augmented Generation               | 🔒 Planificado |
| 4️⃣     | Agentes de IA con herramientas externas            | 🔒 Planificado |

Cada módulo es independiente y puede ejecutarse por separado.

---

## 🔧 Tecnologías usadas (generales)

- Python 3.10+
- sentence-transformers
- ChromaDB
- LangChain + langchain-community
- Ollama (para LLMs locales)
- FastAPI (más adelante)

---

## 🚀 Cómo clonar y correr

```bash
git clone https://github.com/tu_usuario/ai-lab-modules.git
cd ai-lab-modules/module1_embeddings
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows
pip install -r requirements.txt
python main.py
```

---

## 📂 Estructura del proyecto

```
ai-lab-modules/
├── module1_embeddings/         # ✅ Buscador semántico con Chroma
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── module2_llm_chat/           # 🔜 Chat con modelo local o API
├── module3_rag_retrieval/      # 🔒 RAG sobre documentos reales
├── module4_agents/             # 🔒 Agente con herramientas externas
└── README.md                   # ← Este archivo
```

---

## ✍️ Autor

Este proyecto fue desarrollado por **Alejandro** como parte de su formación práctica en IA aplicada.

> Seguime en GitHub o LinkedIn para ver avances, mejoras y próximos módulos 💡
