from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.config.db import SessionLocal
from src.controllers.admin import procesar_excel_feria, autenticar_admin, generar_pdf_resultados, generar_excel_resultados,crear_admin
from fastapi.responses import JSONResponse, StreamingResponse
from src.schemas.admin import AdminAuth,AdminCreate, AdminResponse

admin_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@admin_router.post("/admin/crear", response_model=AdminResponse)
def crear_admin_endpoint(admin: AdminCreate, db: Session = Depends(get_db)):
    return crear_admin(db, admin)

@admin_router.post("/admin/upload_excel", status_code=200)
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx)")
    try:
        resultado = procesar_excel_feria(file, db)
        return {"message": "Datos cargados correctamente", "detalle": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    
    
@admin_router.post("/admin/login", response_class=JSONResponse, status_code=status.HTTP_200_OK)
def autenticar_admin_endpoint(admin_data: AdminAuth, db: Session = Depends(get_db)):
    try:
        admin_info = autenticar_admin(db, admin_data)
        return admin_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@admin_router.get("/admin/resultados/pdf", response_class=StreamingResponse)
def descargar_resultados_pdf(db: Session = Depends(get_db)):
    try:
        pdf_buffer = generar_pdf_resultados(db)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=resultados_votacion.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al generar el PDF de resultados")
    

@admin_router.get("/admin/resultados/excel", response_class=StreamingResponse)
def descargar_resultados_excel(db: Session = Depends(get_db)):
    try:
        excel_buffer = generar_excel_resultados(db)
        return StreamingResponse(
            excel_buffer,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": "attachment; filename=resultados_votacion.xlsx",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el Excel de resultados: {str(e)}")

