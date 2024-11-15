from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.config.db import SessionLocal
from src.controllers import proyecto as proyecto_controller
from src.controllers.proyecto import buscar_proyectos
from src.schemas.proyecto import Proyecto
from typing import List

proyecto_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@proyecto_router.get("/proyectos/{proyecto_id}/votos", response_model=int)
def obtener_cantidad_votos_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    cantidad_votos = proyecto_controller.get_cantidad_votos_proyecto(db, proyecto_id)
    if cantidad_votos is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o sin votos")
    return cantidad_votos

@proyecto_router.get("/proyectos/buscar", response_model=List[Proyecto])
def buscar_proyectos_endpoint(
    nombre: str = Query(..., description="Nombre del proyecto a buscar"),
    db: Session = Depends(get_db)
):
    """
    Buscar proyectos por nombre (case insensitive).
    """
    proyectos = buscar_proyectos(db, nombre)
    if not proyectos:
        raise HTTPException(status_code=404, detail="No se encontraron proyectos")
    return proyectos