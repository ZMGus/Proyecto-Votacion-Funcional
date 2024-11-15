from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from src.models.models import Voto, Proyecto, Categoria
from src.schemas.voto import VotosRestantesResponse
from datetime import datetime, timezone
from typing import Optional
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.models import Voto, Proyecto, Votante
import logging

logger = logging.getLogger(__name__)

def votar_por_proyecto(db: Session, votante_id: int, proyecto_id: int):
        proyecto = db.query(Proyecto).filter_by(id=proyecto_id).first()
        if not proyecto:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        voto_existente = (
            db.query(Voto)
            .join(Proyecto, Proyecto.id == Voto.proyecto_id)
            .filter(Voto.votante_id == votante_id, Proyecto.categoria_id == proyecto.categoria_id)
            .first()
        )
        if voto_existente:
            raise HTTPException(status_code=400, detail="El votante ya tiene un voto en esta categoría")
        fecha_voto = datetime.now(timezone.utc)
        nuevo_voto = Voto(
            votante_id=votante_id, 
            proyecto_id=proyecto_id, 
            fecha_voto=fecha_voto
        )
        db.add(nuevo_voto)
        db.commit()
        db.refresh(nuevo_voto)
        return nuevo_voto
    
def get_votos_todas_categorias(db: Session) -> list:
        resultados = db.query(
            Categoria.nombre_categoria,
            func.coalesce(func.count(Voto.id), 0).label("votos")
        ).join(
            Proyecto, Proyecto.categoria_id == Categoria.id
        ).join(
            Voto, Voto.proyecto_id == Proyecto.id, isouter=True
        ).group_by(
            Categoria.id, Categoria.nombre_categoria
        ).all()
        resultado_list = [{"nombre_categoria": resultado.nombre_categoria, "votos": resultado.votos} for resultado in resultados]
        return resultado_list


def get_votos_todos_proyectos(db: Session) -> list:
    resultados = db.query(
        Proyecto.nombre_proyecto,
        Categoria.nombre_categoria,
        func.coalesce(func.count(Voto.id), 0).label("votos")
    ).join(
        Categoria, Proyecto.categoria_id == Categoria.id
    ).outerjoin(
        Voto, Voto.proyecto_id == Proyecto.id
    ).group_by(
        Proyecto.id, Proyecto.nombre_proyecto, Categoria.nombre_categoria
    ).all()
    resultado_list = [
        {
            "nombre_proyecto": resultado.nombre_proyecto,
            "nombre_categoria": resultado.nombre_categoria,
            "votos": resultado.votos
        } 
        for resultado in resultados
    ]
    return resultado_list

def obtener_porcentaje_participacion(db: Session) -> float:
    total_votantes = db.query(func.count(Votante.id)).scalar()
    if total_votantes == 0:
        return 0.0  
    votantes_unicos = db.query(func.count(func.distinct(Voto.votante_id))).scalar()
    porcentaje_participacion = (votantes_unicos / total_votantes) * 100
    return round(porcentaje_participacion, 2) 


def obtener_datos_combinados(db: Session) -> dict:
    votos_categorias = get_votos_todas_categorias(db)
    votos_proyectos = get_votos_todos_proyectos(db)
    porcentaje_participacion = obtener_porcentaje_participacion(db)
    
    return {
        "votos_categorias": votos_categorias,
        "votos_proyectos": votos_proyectos,
        "porcentaje_participacion": porcentaje_participacion
    }

def verificar_voto_controller(votante_id: int, categoria_id: int, db: Session):
    # Verificar si el usuario ya tiene un voto en la categoría
    voto_existente = (
        db.query(Voto)
        .join(Proyecto, Proyecto.id == Voto.proyecto_id)
        .filter(Voto.votante_id == votante_id, Proyecto.categoria_id == categoria_id)
        .first()
    )
    # Retornar un objeto indicando si ya ha votado
    return {"ha_votado": voto_existente is not None}

def obtener_votos_restantes(db: Session, votante_id: int) -> VotosRestantesResponse:
    # Verificar si el votante existe
    votante = db.query(Votante).filter_by(id=votante_id).first()
    if not votante:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    # Calcular votos restantes
    total_categorias = db.query(Categoria).count()
    votos_realizados = (
        db.query(Voto)
        .join(Proyecto)
        .filter(Voto.votante_id == votante_id)
        .distinct(Proyecto.categoria_id)
        .count()
    )
    votos_restantes = total_categorias - votos_realizados
    return VotosRestantesResponse(votosRestantes=votos_restantes)