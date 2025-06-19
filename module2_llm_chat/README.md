# 🧠 Módulo 2 — Chat con Mistral (Ollama) + Historial en SQLite

Este módulo implementa un chatbot local utilizando un modelo LLM (como `mistral`) ejecutado en Ollama, con persistencia de historial en SQLite y control del contexto por tokens.

---

## ✨ Funcionalidades

- Chat por consola usando `Ollama` como backend local
- Soporte para recordar conversaciones pasadas (contexto)
- Borrado de historial con comando especial (`borrar historial`)
- Control automático del largo del prompt (evita cuelgues)
- Contador de tokens usando `tiktoken`

---

## 🚀 Cómo usar

### 1. Activá el entorno virtual (si no lo hiciste):

```bash
source env/Scripts/activate  # Windows Git Bash
```
