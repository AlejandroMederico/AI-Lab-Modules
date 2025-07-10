from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.linkedin.schemas import MessageRequest, BusquedaRequest, Empleo
from backend.linkedin.service import LinkedinService
import asyncio
from backend.linkedin.cookies import guardar_cookies
from typing import List

router = APIRouter(prefix="/linkedin", tags=["linkedin"])


@router.post("/message")
async def enviar_mensaje_linkedin(data: MessageRequest):
    service = await LinkedinService.crear_desde_cookies()
    if not service:
        raise HTTPException(
            status_code=500, detail="No se pudo iniciar sesión con cookies"
        )

    try:
        print("📬 Enviando mensaje...")
        result = await service.enviar_mensaje(data)
        print("✅ Resultado:", result)
        return {"status": "mensaje enviado"}
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.cerrar_navegador()


@router.post("/check-login")
async def check_login():
    service = await LinkedinService.crear_desde_cookies()
    if not service:
        return {
            "error": "No se pudo iniciar sesión en LinkedIn o el navegador no se cargó correctamente."
        }

    try:
        result = await service.check_login()
        return {"ok": result}
    finally:
        await asyncio.sleep(5)
        await service.cerrar_navegador()


@router.post("/save-cookies")
async def save_cookies():
    try:
        print("🟡 Abriendo navegador para guardar cookies...")
        service = await LinkedinService.crear_navegador_manual()
        input("🔵 Iniciá sesión y presioná Enter para continuar...")
        cookies = await service.context.cookies()
        guardar_cookies(cookies)
        return {"message": "Cookies guardadas exitosamente"}
    except Exception as e:
        print(f"❌ Error al guardar cookies: {e}")
        return {"error": str(e)}
    finally:
        await service.cerrar_navegador()

@router.post("/buscar", response_model=List[Empleo])
async def buscar_empleos_endpoint(data: BusquedaRequest):
    agente = None
    try:
        # Convertimos el modelo a dict
        filtros = data.dict(exclude_none=True)

        # Extraemos rol y ubicación del dict
        rol = filtros.pop("rol", "Desarrollador IA")
        ubicacion = filtros.pop("ubicacion", "Argentina")

        # Creamos el servicio con sesión activa
        agente = await LinkedinService.crear_desde_cookies()
        if not agente:
            raise HTTPException(status_code=500, detail="No se pudo crear sesión con cookies")

        # Primero hacemos búsqueda base (para que aparezcan los filtros)
        await agente.realizar_busqueda_inicial(rol, ubicacion)
        print("🔍 Iniciando búsqueda...")
        resultados = await agente.buscar_empleos_por_filtros(filtros)
        print(f"✅ {len(resultados)} empleos encontrados")
        return resultados

    except Exception as e:
        print(f"❌ Error durante la búsqueda: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if agente:
            await agente.cerrar_navegador()



