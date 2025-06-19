# tokens.py
import tiktoken


def contar_tokens(texto: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(texto))
