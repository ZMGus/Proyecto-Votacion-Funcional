from pydantic import BaseModel
from typing import List, Optional
from src.schemas.categoria import Categoria

class FeriaBase(BaseModel):
    numero_feria: int
    anno: int
    lugar: str

class FeriaCreate(FeriaBase):
    pass

class Feria(FeriaBase):
    id: int
    categorias: List[Categoria] = [] 

    class Config:
        orm_mode = True
