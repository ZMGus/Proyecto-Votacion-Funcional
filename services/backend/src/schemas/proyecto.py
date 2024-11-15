from pydantic import BaseModel
from typing import Optional

class ProyectoBase(BaseModel):
    nombre_proyecto: str
    descripcion_proyecto: Optional[str] = None
    nombre_pre_empresa: Optional[str] = None
    logo: Optional[str]
   

class ProyectoCreate(ProyectoBase):
    categoria_id: int

class Proyecto(ProyectoBase):
    id: int

    class Config:
        orm_mode = True