from pydantic import BaseModel
from typing import List, Optional
from src.schemas.proyecto import Proyecto

class CategoriaBase(BaseModel):
    nombre_categoria: str
    descripcion_categoria: Optional[str]
    imagen: Optional[str]

class CategoriaCreate(CategoriaBase):
    feria_id: int

class Categoria(CategoriaBase):
    id: int
    proyectos: List['Proyecto'] = []

    class Config:
        orm_mode = True