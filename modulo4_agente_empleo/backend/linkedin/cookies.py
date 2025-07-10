import json


def cargar_cookies(path: str = "backend/credentials/linkedin_cookies.json") -> list:
    with open(path, "r") as f:
        return json.load(f)


def limpiar_cookies(cookies: list) -> list:
    for cookie in cookies:
        if "sameSite" in cookie:
            if cookie["sameSite"] not in ("Strict", "Lax", "None"):
                del cookie["sameSite"]
    return cookies


def guardar_cookies(cookies):
    with open("backend/credentials/linkedin_cookies.json", "w") as f:
        json.dump(cookies, f, indent=2)
    print("✅ Cookies guardadas correctamente")
