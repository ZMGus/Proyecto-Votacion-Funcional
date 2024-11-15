from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VotoBase(BaseModel):
    votante_id: int
    proyecto_id: int

    class Config:
        orm_mode = True

class VotoCreate(VotoBase):
    pass

class Voto(VotoBase):
    id: int

    class Config:
        orm_mode = True

class VerificarVotoResponse(BaseModel):
    ha_votado: bool

    class Config:
        orm_mode = True
        
class VotosRestantesResponse(BaseModel):
    votosRestantes: int

    class Config:
        orm_mode = True