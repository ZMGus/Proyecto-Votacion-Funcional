from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.schemas.votante import VotanteCreate,Votante_schema,VotanteCodigoResponse
from src.controllers import votante as votante_controller
from src.controllers.votante import autenticar_votante
from src.config.db import SessionLocal
import logging
from src.schemas.votante import VotanteAuth
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

votante_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@votante_router.post("/votante/ingreso", response_class=JSONResponse, status_code=status.HTTP_200_OK)
def autenticar_votante_endpoint(votante_data: VotanteAuth, db: Session = Depends(get_db)):
    try:
        response = autenticar_votante(db, votante_data)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
@votante_router.post("/votante/rut/{rut}", response_model=Votante_schema, status_code=status.HTTP_200_OK)
def get_votante_by_rut(rut: int, db: Session = Depends(get_db)):
    '''
    Obtiene un votante mediante el rut (sin el digito verificador).
    
    Parametros:
    - db: la sesion de la base de datos
    - rut: el rut sin el dv
    
    Returns:
    - la información de un votante
    '''
    try:
        votante = votante_controller.get_votante_by_rut(db, rut)
        return votante
    except Exception as e:
        if str(e) == "User not found":
            return Response(content=str(e), status_code=status.HTTP_404_NOT_FOUND)
        else:
            return Response(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@votante_router.post("/votante", response_model=Votante_schema)
def create_votante(votante: VotanteCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el RUT ya está registrado
        db_votante = votante_controller.get_votante_by_rut(db, rut=votante.rut)
        if db_votante:
            raise HTTPException(status_code=400, detail="El RUT ya está registrado")

        # Crear el votante y generar el código automáticamente
        created_votante = votante_controller.create_votante(db=db, votante=votante)
        # Retornar el votante completo, incluyendo el `codigo_acceso`
        return created_votante
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el votante")

@votante_router.get("/votantes/{votante_id}/votos", response_model=list[Votante_schema])
def obtener_votos_por_votante(votante_id: int, db: Session = Depends(get_db)):
    votos = votante_controller.get_votos_por_votante(db, votante_id)
    if not votos:
        raise HTTPException(status_code=404, detail="No se encontraron votos para este votante")
    return votos

@votante_router.get("/votante/codigo", response_model=VotanteCodigoResponse)
def obtener_codigo_acceso(rut: str, dv: str, db: Session = Depends(get_db)):
    votante = votante_controller.get_votante_by_rut_dv(db, rut, dv)
    if not votante:
        raise HTTPException(status_code=404, detail="Votante no encontrado")
    return {"codigo_acceso": votante.codigo_acceso}