from sqlalchemy.orm import Session
from src.models.models import Proyecto

def get_proyectos_por_categoria(db: Session, categoria_id: int):
    proyectos = db.query(Proyecto).filter(Proyecto.categoria_id == categoria_id).all()
    return proyectos
