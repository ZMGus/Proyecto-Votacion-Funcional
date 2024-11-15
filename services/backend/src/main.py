
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.db import engine, Base, SessionLocal
from .routers.votante import votante_router
from .routers.categoria import categoria_router
from .routers.feria import feria_router
from .routers.proyecto import proyecto_router
from .routers.voto import voto_router
from .routers.admin import admin_router
from src.initial_data import load_initial_data
from src.models.models import *
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Intentando conectar a la base de datos y crear tablas...")
for table_name in Base.metadata.tables.keys():
    logger.info(f"Tabla registrada: {table_name}")

try:
    logger.info("Eliminando y recreando las tablas...")
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas exitosamente.")
except Exception as e:
    logger.error(f"Error al crear las tablas: {e}")
    raise e

with SessionLocal() as db:
    logger.info("Insertando datos iniciales...")
    #load_initial_data()
    logger.info("Datos iniciales insertados exitosamente.")


# Inicializar la aplicación de FastAPI
app = FastAPI()
origins = [
    "http://localhost:4200",  # Permitir el frontend local
    "http://127.0.0.1:4200" 
    "http://votacion.feriadesoftware.cl"
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(votante_router)
app.include_router(proyecto_router)
app.include_router(categoria_router)
app.include_router(feria_router)
app.include_router(voto_router)
app.include_router(admin_router)