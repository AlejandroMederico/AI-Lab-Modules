import sqlite3
import datetime

DB_FILE = "chat_history.db"


def init_db():
    """Crea (si no existe) y abre la BD para el historial."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT NOT NULL,   -- 'user' o 'assistant'
            content   TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        """
    )
    conn.commit()
    return conn, cur


def save_message(cur, role: str, content: str):
    """Guarda un turno en la tabla."""
    cur.execute(
        "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
        (role, content, datetime.datetime.utcnow().isoformat()),
    )


def load_history(cur):
    """Devuelve el historial completo ordenado."""
    rows = cur.execute("SELECT role, content FROM messages ORDER BY id").fetchall()
    return [{"role": r, "content": c} for r, c in rows]
