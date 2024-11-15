from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.db import SessionLocal
from src.controllers.voto import votar_por_proyecto,get_votos_todas_categorias, get_votos_todos_proyectos, obtener_porcentaje_participacion,obtener_datos_combinados, verificar_voto_controller, obtener_votos_restantes
from src.schemas.voto import VotoCreate, Voto, VerificarVotoResponse, VotosRestantesResponse
from src.models.models import Voto as VotoModel
import logging
from typing import List, Dict, Any
logger = logging.getLogger(__name__)
voto_router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@voto_router.post("/votar", response_model=Voto, status_code=status.HTTP_201_CREATED)
def votar(voto: VotoCreate, db: Session = Depends(get_db)):
    try:
        nuevo_voto = votar_por_proyecto(
            db=db, 
            votante_id=voto.votante_id, 
            proyecto_id=voto.proyecto_id
        )
        return nuevo_voto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@voto_router.get("/categorias/votos", response_model=List[Dict[str, Any]])
def obtener_votos_todas_categorias(db: Session = Depends(get_db)):
    try:
        logger.debug("Llamada a obtener_votos_todas_categorias")
        votos_por_categoria = get_votos_todas_categorias(db)
        
        if not votos_por_categoria:
            raise HTTPException(status_code=404, detail="No hay categorías para contar votos")

        logger.debug(f"Votos por categoría obtenidos: {votos_por_categoria}")
        return votos_por_categoria
    except Exception as e:
        logger.error(f"Error al obtener votos por categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener votos por categoría")


@voto_router.get("/proyectos/votos", response_model=List[Dict[str, Any]])
def obtener_votos_todos_proyectos(db: Session = Depends(get_db)):
    try:
        votos_por_proyecto = get_votos_todos_proyectos(db)
        if not votos_por_proyecto:
            raise HTTPException(status_code=404, detail="No hay proyectos para contar votos")
        return votos_por_proyecto
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener votos por proyecto")
    
    
@voto_router.get("/votos/participacion", response_model=float)
def obtener_participacion(db: Session = Depends(get_db)):
    try:
        participacion = obtener_porcentaje_participacion(db)
        return participacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el porcentaje de participación: {str(e)}")
    

@voto_router.get("/votos/datos", response_model=dict)
def obtener_datos_votos_y_participacion(db: Session = Depends(get_db)):
    try:
        logger.debug("Llamada a obtener_datos_votos_y_participacion")
        datos = obtener_datos_combinados(db)
        
        if not datos["votos_categorias"] and not datos["votos_proyectos"]:
            raise HTTPException(status_code=404, detail="No hay datos de votos disponibles")

        logger.debug(f"Datos de votos y participación obtenidos: {datos}")
        return datos
    except Exception as e:
        logger.error(f"Error al obtener datos de votos y participación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener datos de votos y participación")



@voto_router.get("/votos/verificar/{votante_id}/{categoria_id}", response_model=VerificarVotoResponse)
def verificar_voto(votante_id: int, categoria_id: int, db: Session = Depends(get_db)):
    return verificar_voto_controller(votante_id, categoria_id, db)

@voto_router.get("/votos/verificar-completados/{votante_id}", response_model=VotosRestantesResponse)
def verificar_votos_completados(votante_id: int, db: Session = Depends(get_db)):
    try:
        return obtener_votos_restantes(db, votante_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al verificar los votos completados")