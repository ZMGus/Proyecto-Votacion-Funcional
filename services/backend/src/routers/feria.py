from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.config.db import SessionLocal
from typing import Optional, List
from src.controllers.feria import get_categorias_feria_actual, borrar_feria, obtener_feria_actual
from src.schemas.categoria import Categoria as CategoriaSchema
from src.schemas.feria import Feria as FeriaSchema



import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


feria_router = APIRouter()


def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@feria_router.get("/ferias/categorias", response_model=List[CategoriaSchema])
def obtener_categorias_feria_actual(db: Session = Depends(get_db)):
    categorias = get_categorias_feria_actual(db)
    if not categorias:
        return []  # Devolver una lista vacía si no hay categorías
    return categorias

        
@feria_router.get("/ferias/categorias", response_model=List[CategoriaSchema])
def obtener_categorias_feria_actual(db: Session = Depends(get_db)):
    categorias = get_categorias_feria_actual(db)
    if not categorias:
        raise HTTPException(status_code=404, detail="No se encontraron categorías para esta feria")
    return categorias

@feria_router.get("/feria", response_model=FeriaSchema)
def obtener_feria_actual_endpoint(db: Session = Depends(get_db)):
    feria = obtener_feria_actual(db)
    if not feria:
        raise HTTPException(status_code=404, detail="No se encontró la feria principal")
    return feria

@feria_router.get("/feria", response_model=FeriaSchema)
def obtener_feria_actual_endpoint(db: Session = Depends(get_db)):
    feria = obtener_feria_actual(db)
    if not feria:
        raise HTTPException(status_code=404, detail="No se encontró la feria principal")
    return feria
    
    
@feria_router.delete("/ferias/{feria_id}", status_code=status.HTTP_200_OK)
def eliminar_feria(feria_id: int, db: Session = Depends(get_db)):
    try:
        return borrar_feria(db, feria_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
