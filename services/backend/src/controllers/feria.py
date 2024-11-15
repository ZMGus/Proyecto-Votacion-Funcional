from src.models.models import Categoria, Feria
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

def get_categorias_feria_actual(db: Session) -> List[Categoria]:
    feria = db.query(Feria).filter(Feria.id == 1).first()
    if not feria:
        raise HTTPException(status_code=404, detail="No se encontró la feria principal.")

    # Asegúrate de que siempre devuelva una lista
    categorias = db.query(Categoria).filter(Categoria.feria_id == feria.id).all()
    return categorias if categorias else []


def obtener_feria_actual(db: Session) -> Feria:
    feria = db.query(Feria).filter(Feria.id == 1).first()  # Asumimos que siempre es la feria con ID 1
    if not feria:
        raise HTTPException(status_code=404, detail="No se encontró la feria principal.")
    return feria

def borrar_feria(db: Session, feria_id: int):
    feria = db.query(Feria).filter(Feria.id == feria_id).first()
    if not feria:
        raise HTTPException(status_code=404, detail="Feria no encontrada")
    db.delete(feria)
    db.commit()
    return {"message": "Feria eliminada exitosamente"}