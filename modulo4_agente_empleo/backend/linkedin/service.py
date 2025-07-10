import json
from playwright.async_api import async_playwright
from backend.linkedin.cookies import cargar_cookies, limpiar_cookies
from backend.linkedin.schemas import MessageRequest, BusquedaRequest, Empleo
from typing import List

LINKEDIN_URL = "https://www.linkedin.com"


class LinkedinService:
    def __init__(self, context, browser, page):
        self.context = context
        self.browser = browser
        self.page = page

    @classmethod
    async def crear_desde_cookies(cls):
        print("🟡 Creando sesión con cookie manual...")
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()

        cookies = cargar_cookies()
        if cookies:
            await context.add_cookies(cookies)

        page = await context.new_page()

        return cls(context, browser, page)

    @classmethod
    async def crear_navegador_manual(cls):
        print("🟡 Abriendo navegador para guardar cookies...")
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"{LINKEDIN_URL}/login")
        return cls(context, browser, page)

    async def check_login(self):
        await self.page.goto(f"{LINKEDIN_URL}/feed")
        await self.page.wait_for_timeout(3000)
        return "feed" in self.page.url

    async def enviar_mensaje(self, data: MessageRequest):
        print("🟡 Navegando al perfil...")
        await self.page.goto(data.perfil_url, wait_until="domcontentloaded")
        await self.page.wait_for_timeout(4000)

        if "/messaging/thread/" not in data.perfil_url:
            print("🟡 Clickeando en 'Mensaje'...")
            boton = await self.page.get_by_role("button", name="Mensaje")
            if boton:
                await boton.click()
                await self.page.wait_for_timeout(3000)

        print("🟡 Buscando caja de texto...")
        cuadro = await self.page.query_selector("div[role='textbox']")
        if not cuadro:
            raise Exception("No se encontró la caja de mensaje")

        await cuadro.type(data.mensaje, delay=50)
        await self.page.wait_for_timeout(1000)

        # 👇 Nuevo: Click explícito en botón "Enviar"
        boton_enviar = await self.page.query_selector("button.msg-form__send-button")
        if boton_enviar:
            await boton_enviar.click()
            print("✅ Click en botón 'Enviar'")
        else:
            raise Exception("No se encontró el botón de envío")

        print("✅ Mensaje enviado con éxito")
        return {"ok": True}

    async def cerrar_navegador(self):
        print("🧹 Cerrando navegador...")
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def buscar_empleos_por_filtros(self, filtros: BusquedaRequest):
        print("⚙️ Aplicando filtros de búsqueda...")
        print(f"🧪 Filtros recibidos: {filtros}")
        page = self.page

        await LinkedinService.aplicar_filtro_radio(
            page=page,
            boton_id="searchFilter_timePostedRange",
            opciones={
                "Cualquier momento": "timePostedRange-r0",
                "Mes pasado": "timePostedRange-r2592000",
                "Semana pasada": "timePostedRange-r604800",
                "Últimas 24 horas": "timePostedRange-r86400",
            },
            valor_usuario=filtros.get("fecha_publicacion"),
            index_boton=0,
            nombre_filtro="fecha de publicación",
        )

        await LinkedinService.aplicar_filtro_radio(
            page=page,
            boton_id="searchFilter_experience",
            opciones={
                "Practicas": "experience-1",
                "Sin experiencia": "experience-2",
                "Algo de responsabilidad": "experience-3",
                "Intermedio": "experience-4",
                "Director": "experience-5",
                "Ejecutivo": "experience-6",
            },
            valor_usuario=filtros.get("experiencia"),
            index_boton=1,
            nombre_filtro="nivel de experiencia",
        )

        await LinkedinService.aplicar_filtro_radio(
            page=page,
            boton_id="searchFilter_workplaceType",
            opciones={
                "Presencial": "workplaceType-1",
                "En Remoto": "workplaceType-2",
                "Hibrido": "workplaceType-3",
            },
            valor_usuario=filtros.get("modalidad"),
            index_boton=3,
            nombre_filtro="modalidad de trabajo",
        )

        print("🔍 Extrayendo resultados de la lista...")
        resultados = await LinkedinService.extraer_resultados_empleo(self.page)

        return resultados

    async def extraer_resultados_empleo(page) -> List[Empleo]:
        # Esperamos a que estén disponibles los resultados visibles
        await page.wait_for_selector("li.scaffold-layout__list-item", timeout=20000)
        elementos = await page.query_selector_all("li.scaffold-layout__list-item")

        print(f"🔍 Extrayendo resultados de la lista... ({len(elementos)} encontrados)")

        resultados = []

        for li in elementos:
            try:
                # titulo = await li.eval_on_selector(
                #     "a strong", "el => el.textContent?.trim()"
                # )
                link = await li.eval_on_selector(
                    "a[href*='/jobs/view/']", "el => el.href"
                )
                # empresa = await li.eval_on_selector(
                #     ".job-card-container__company-name", "el => el.textContent?.trim()"
                # )
                # ubicacion = await li.eval_on_selector(
                #     ".job-card-container__metadata span", "el => el.textContent?.trim()"
                # )
                # fecha = await li.eval_on_selector(
                #     ".job-search-card__listdate", "el => el.textContent?.trim()"
                # )

                empleo = Empleo(
                    titulo="N/A",
                    empresa="N/A",
                    ubicacion="N/A",
                    modalidad=None,
                    fecha="N/A",
                    link=link or "#",
                )
                resultados.append(empleo)

            except Exception as e:
                print(f"⚠️ Error extrayendo un resultado: {e}")
                continue

        print(f"✅ {len(resultados)} empleos encontrados")
        return resultados

    async def aplicar_filtro_radio(
        page,
        boton_id: str,
        opciones: dict,
        valor_usuario: str,
        index_boton: int,
        nombre_filtro: str,
    ):
        try:
            await page.wait_for_selector(f"button#{boton_id}", timeout=10000)
            await page.click(f"button#{boton_id}")
            await page.wait_for_timeout(1000)
        except Exception as e:
            print(f"⚠️ No se pudo abrir el filtro '{nombre_filtro}': {e}")
            return

        input_id = opciones.get(valor_usuario)

        if input_id:
            try:
                js_click_label = f"""
                    document.querySelector("label[for='{input_id}']")?.click();
                """
                await page.evaluate(js_click_label)
                await page.wait_for_timeout(1000)

                try:
                    locator = page.locator(
                        "button[aria-label^='Aplicar el filtro actual para mostrar']"
                    ).nth(index_boton)
                    await locator.wait_for(state="visible", timeout=10000)
                    await locator.click()
                    await page.wait_for_timeout(3000)
                except Exception as fallback_error:
                    print(
                        f"🔁 Intentando con JavaScript como fallback: {fallback_error}"
                    )
                    js_click_visible = """
                        Array.from(document.querySelectorAll("button[aria-label^='Aplicar el filtro actual para mostrar']"))
                            .find(btn => btn.offsetParent !== null)?.click();
                    """
                    await page.evaluate(js_click_visible)
                    await page.wait_for_timeout(1000)
            except Exception as e:
                print(f"❌ Error al aplicar el filtro '{valor_usuario}': {e}")
        else:
            print(f"⚠️ Valor no reconocido para '{nombre_filtro}': {valor_usuario}")

    async def leer_resultados(self) -> list[dict]:
        print("📄 Leyendo resultados de búsqueda...")
        page = self.page
        await page.wait_for_selector("ul.jobs-search__results-list", timeout=10000)

        resultados = []

        tarjetas = await page.query_selector_all("ul.jobs-search__results-list li")

        for tarjeta in tarjetas:
            try:
                titulo = await tarjeta.query_selector_eval("h3", "el => el.innerText")
                empresa = await tarjeta.query_selector_eval("h4", "el => el.innerText")
                ubicacion = await tarjeta.query_selector_eval(
                    ".job-search-card__location", "el => el.innerText"
                )
                fecha = await tarjeta.query_selector_eval("time", "el => el.innerText")
                link = await tarjeta.query_selector_eval(
                    "a.job-card-container__link", "el => el.href"
                )

                resultados.append(
                    {
                        "titulo": titulo.strip(),
                        "empresa": empresa.strip(),
                        "ubicacion": ubicacion.strip(),
                        "modalidad": None,  # Se puede agregar luego con scraping extra
                        "fecha": fecha.strip(),
                        "link": link.strip(),
                    }
                )
            except Exception as e:
                print("⚠️ Error leyendo una tarjeta:", e)
                continue

        print(f"✅ {len(resultados)} resultados encontrados.")
        return resultados

    async def realizar_busqueda_inicial(self, rol: str, ubicacion: str):
        print(f"🔎 Realizando búsqueda inicial: {rol} en {ubicacion}")
        page = self.page

        await page.goto("https://www.linkedin.com/jobs")

        # Esperar a los inputs (usan ember dinámico, por eso usamos id^=)
        await page.wait_for_selector(
            "input[id^='jobs-search-box-keyword-id']", timeout=10000
        )
        await page.wait_for_selector(
            "input[id^='jobs-search-box-location-id']", timeout=10000
        )

        # Completar campos
        await page.fill("input[id^='jobs-search-box-keyword-id']", rol)
        await page.fill("input[id^='jobs-search-box-location-id']", ubicacion)

        # Presionar Enter para ejecutar la búsqueda
        await page.keyboard.press("Enter")

        # Esperar que la URL cambie y la página cargue resultados
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(3000)
