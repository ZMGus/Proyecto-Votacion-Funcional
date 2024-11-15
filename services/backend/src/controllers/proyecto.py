from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.models import Voto, Proyecto
from typing import List

def get_cantidad_votos_proyecto(db: Session, proyecto_id: int) -> int:
    cantidad_votos = db.query(func.count(Voto.id)).filter(Voto.proyecto_id == proyecto_id).scalar()
    return cantidad_votos


def buscar_proyectos(db: Session, nombre: str) -> List[Proyecto]:
    """
    Buscar proyectos que coincidan parcialmente con el nombre (insensible a mayúsculas y minúsculas).
    """
    query = db.query(Proyecto).filter(func.lower(Proyecto.nombre_proyecto).ilike(f"%{nombre.lower()}%"))
    proyectos = query.all()
    return proyectos