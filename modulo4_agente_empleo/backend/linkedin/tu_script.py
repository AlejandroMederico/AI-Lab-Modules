import asyncio
import json
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

LI_AT = (
    os.getenv("LINKEDIN_LI_AT")
    or "AQEDASksteYCQ__lAAABl7QYIc0AAAGX2CSlzU0AZcx_UmbZ_itITgblLbpONT8IlSQhsGzXY5jUZO6tVSXUSrjX_YT3MstE12qWadLLkWe-UEL-S9C0jSM4i94TG1HDZH89GUj6nwcW6iyH40G1DeIR"
)


async def probar_cookie():
    print("🟡 Abriendo LinkedIn con cookies...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # ✅ Cargar cookies desde ../credentials/linkedin_cookies.json
        with open("../credentials/linkedin_cookies.json", "r") as f:
            cookies = json.load(f)

        cookies = limpiar_cookies(cookies)
        print("🟢 Cookies cargadas:")
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        print("🔵 Título:", await page.title())
        await asyncio.sleep(5)
        await browser.close()


def limpiar_cookies(cookies: list) -> list:
    for cookie in cookies:
        if "sameSite" in cookie:
            if cookie["sameSite"] not in ("Strict", "Lax", "None"):
                del cookie["sameSite"]
    return cookies


async def enviar_mensaje(perfil_url: str, mensaje: str):
    print("🟡 Enviando mensaje desde cookies...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # ✅ Cargar y limpiar cookies
        with open("../credentials/linkedin_cookies.json", "r") as f:
            cookies = json.load(f)
        print("🟢 Cookies cargadas:")
        cookies = limpiar_cookies(cookies)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(perfil_url)
        await page.wait_for_timeout(4000)

        # Si no es un thread de mensaje directo, abrimos ventana de mensaje
        if "/messaging/thread/" not in perfil_url:
            print("🟡 Clickeando en 'Mensaje'...")
            await page.get_by_role("button", name="Mensaje").click()
            await page.wait_for_timeout(3000)

        print("🟡 Buscando caja de texto...")
        cuadro = await page.query_selector("div[role='textbox']")
        if not cuadro:
            print("❌ No se encontró la caja de mensaje")
            return

        await cuadro.type(mensaje)
        await page.keyboard.press("Enter")
        print("✅ Mensaje enviado con éxito")

        await context.close()
        await browser.close()


async def guardar_cookies():
    print("🟡 Abriendo navegador para que inicies sesión...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/login")
        print("🔵 Iniciá sesión manualmente y luego presioná Enter en esta terminal...")
        input("⏳ Esperando a que presiones Enter...")

        cookies = await context.cookies()
        with open("../credentials/linkedin_cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)

        print("✅ Cookies guardadas correctamente")
        await browser.close()


if __name__ == "__main__":

    asyncio.run(guardar_cookies())
    # Cambiá estos valores para probar
    url = "https://www.linkedin.com/messaging/thread/2-YmIyMzYxNTctODBhYS00ODgxLWI5YzEtN2NkMjZhZmM5NWRjXzAxMg==/"  # o perfil de usuario
    msg = "Hola, REINA JAIZITA SOY UN HACKER 😄"

    # asyncio.run(probar_cookie())
    # asyncio.run(enviar_mensaje(url, msg))
