
from sqlalchemy.orm import Session
from src.schemas.votante import VotanteBase
from src.models.models import Votante, Voto
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from src.schemas.votante import VotanteAuth
import random
import string

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def autenticar_votante(db: Session, votante_data: VotanteAuth):
    votante = (
        db.query(Votante)
        .filter_by(rut=votante_data.rut, dv=votante_data.dv, codigo_acceso=votante_data.codigo_acceso)
        .first()
    )

    if not votante:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    votante_info = {
        "id_votante": votante.id,
        "rut_completo": f"{votante.rut}-{votante.dv}",
        "nombre": votante.nombre,
        "apellido": votante.apellido,
        "email": votante.email,
        "codigo_acceso": votante.codigo_acceso,
        "estado_codigo": votante.estado_codigo
    }
    return JSONResponse(content={"message": "Ingreso exitoso", "votante": votante_info, "statusCode": 200})


def get_votante_by_rut(db: Session, rut: int):
    '''
    Obtiene un votante mediante el rut (sin el digito verificador).
    
    Parametros:
    - db: la sesion de la base de datos
    - rut: el rut sin el dv
    
    Returns:
    - la información de un votante
    '''
    votante = db.query(Votante).filter(Votante.rut == rut).first()
    return votante

    
def generar_codigo_acceso() -> str:
    """Genera un código alfanumérico de 8 caracteres."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_votante(db: Session, votante: VotanteBase):
    try:
        # Generar un código de acceso único
        codigo_acceso = generar_codigo_acceso()
        db_votante = Votante(
            rut=votante.rut,
            dv=votante.dv,
            nombre=votante.nombre,
            apellido=votante.apellido,
            email=votante.email,
            codigo_acceso=codigo_acceso,
            estado_codigo=False
        )
        db.add(db_votante)
        db.commit()
        db.refresh(db_votante)
        return db_votante
    except SQLAlchemyError as e:
        logger.error(f"Error al intentar crear el votante en la base de datos: {e}")
        raise
    
def get_votos_por_votante(db: Session, votante_id: int):
    votos = db.query(Voto).filter(Voto.votante_id == votante_id).all()
    return votos

def get_votante_by_rut_dv(db: Session, rut: str, dv: str):
    return db.query(Votante).filter(Votante.rut == rut, Votante.dv == dv).first()