from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.categoria import Categoria,Proyecto
from src.controllers import categoria as categoria_controller
from src.config.db import SessionLocal

categoria_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@categoria_router.get("/categorias/{categoria_id}/proyectos", response_model=list[Proyecto])
def obtener_proyectos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    proyectos = categoria_controller.get_proyectos_por_categoria(db, categoria_id)
    if not proyectos:
        raise HTTPException(status_code=404, detail="No se encontraron proyectos para esta categoría")
    return proyectos