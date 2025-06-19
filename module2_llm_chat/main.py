import requests
import json
import tiktoken

from db_utils import init_db, load_history, save_message
from tokens import contar_tokens


MAX_CTX = 1000  # tope (en tokens) para el prompt


def build_prompt_limited(history):
    """
    Devuelve (prompt_recortado, history_recortado).

    Si el prompt supera MAX_CTX tokens, recorta los 2 turnos más viejos
    y vuelve a probar hasta quedar por debajo del límite.
    """
    prompt = construir_prompt_con_historial(history)
    while contar_tokens(prompt) > MAX_CTX and len(history) > 2:
        history = history[2:]  # descarta el turno de usuario + asistente más antiguos
        prompt = construir_prompt_con_historial(history)
    return prompt, history


def construir_prompt_con_historial(history):
    prompt = ""
    for t in history:
        role, content = t["role"], t["content"]
        if role == "user":
            prompt += f"Usuario: {content}\n"
        else:
            prompt += f"Asistente: {content}\n"
    return prompt + "Asistente: "


def contar_tokens(texto: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(texto))


def borrar_historial(conn, cur):
    cur.execute("DELETE FROM messages")
    conn.commit()
    print("🗑️  Historial borrado correctamente.")
    return []


def chat_with_mistral():
    print(
        "\n🤖 Chat con Mistral (Ollama + SQLite) — escribí 'salir' para terminar o 'borrar historial' para limpiar"
    )

    conn, cur = init_db()
    history = load_history(cur)

    while True:
        prompt = input("\n🧑 Tú: ")
        p_low = prompt.lower().strip()

        if p_low in {"salir", "exit", "quit"}:
            print("👋 Hasta luego!")
            break

        if p_low in {"borrar historial", "reset"}:
            history = borrar_historial(conn, cur)
            continue

        save_message(cur, "user", prompt)
        conn.commit()

        full_prompt, history = build_prompt_limited(
            history + [{"role": "user", "content": prompt}]
        )

        print(f"\n🔢 Prompt actual tiene {contar_tokens(full_prompt)} tokens")
        print("🪵 DEBUG: Prompt enviado:\n" + full_prompt[:1000])

        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": full_prompt, "stream": True},
                stream=True,
                timeout=300,
            )
            resp.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 500:
                print(
                    "💥 Error interno en Ollama (500). Posiblemente por prompt demasiado grande o bug en el modelo."
                )
                print("🪵 Último prompt generado (recortado):\n", full_prompt[:1000])
            raise
        except requests.RequestException as e:
            print(f"⚠️  Error al llamar a Ollama: {e}")
            continue

        print("🤖 Mistral: ", end="", flush=True)
        full_response = ""

        for line in resp.iter_lines():
            if not line:
                continue
            try:
                obj = json.loads(line.decode("utf-8"))
                token = obj.get("response", "")
                print(token, end="", flush=True)
                full_response += token
            except json.JSONDecodeError:
                continue
        print("\n")

        save_message(cur, "assistant", full_response)
        conn.commit()
        history.extend(
            [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": full_response},
            ]
        )


if __name__ == "__main__":
    chat_with_mistral()
