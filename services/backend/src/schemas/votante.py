from pydantic import BaseModel
from typing import Optional
from datetime import time, datetime


class VotanteBase(BaseModel):
    rut: int
    dv: str
    nombre: str
    apellido: str
    email: str
    
class VotanteAuth(BaseModel):
    rut: int
    dv: str
    codigo_acceso: str

class VotanteCreate(VotanteBase):
    pass

class Votante_schema(VotanteBase):
    id: int
    codigo_acceso: str
    estado_codigo: bool
    fecha_registro: datetime

    class Config:
        orm_mode = True
        
class VotanteCodigoResponse(BaseModel):
    codigo_acceso: str