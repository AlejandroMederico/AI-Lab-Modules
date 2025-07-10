from pydantic import BaseModel
from typing import Optional, List


class MessageRequest(BaseModel):
    perfil_url: str
    mensaje: str


class Empleo(BaseModel):
    titulo: str
    empresa: str
    ubicacion: str
    modalidad: Optional[str]
    fecha: str
    link: str


class BusquedaRequest(BaseModel):
    rol: str = "Desarrollador"
    ubicacion: str = "Argentina"
    fecha_publicacion: Optional[str] = None
    experiencia: Optional[str] = None
    modalidad: Optional[str] = None
