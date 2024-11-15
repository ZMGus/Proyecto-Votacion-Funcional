import pandas as pd
from sqlalchemy.orm import Session
from src.models.models import Feria, Categoria, Proyecto, Admin
from src.schemas.admin import AdminAuth,AdminCreate
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from src.controllers.voto import obtener_datos_combinados

def crear_admin(db: Session, admin: AdminCreate):
    # Verificar si el email ya existe
    admin_existente = db.query(Admin).filter(Admin.email == admin.email).first()
    if admin_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_admin = Admin(
        nombre=admin.nombre,
        apellido=admin.apellido,
        email=admin.email,
        password=admin.password
    )
    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)
    return nuevo_admin

def procesar_excel_feria(file, db: Session):
    try:
        excel_data = pd.ExcelFile(file.file)
        required_sheets = ["Ferias", "Categorias", "Proyectos"]
        for sheet in required_sheets:
            if sheet not in excel_data.sheet_names:
                raise ValueError(f"El archivo debe contener la hoja '{sheet}'")
        
        ferias_df = pd.read_excel(excel_data, sheet_name="Ferias")
        categorias_df = pd.read_excel(excel_data, sheet_name="Categorias")
        proyectos_df = pd.read_excel(excel_data, sheet_name="Proyectos")
        
        if not set(['id', 'numero_feria', 'año', 'lugar']).issubset(ferias_df.columns):
            raise ValueError("La hoja 'Ferias' debe contener las columnas 'id', 'numero_feria', 'año', 'lugar'")
        if not set(['id', 'nombre_categoria', 'descripcion_categoria', 'imagen', 'feria_id']).issubset(categorias_df.columns):
            raise ValueError("La hoja 'Categorias' debe contener las columnas 'id', 'nombre_categoria' y 'feria_id'")
        if not set(['nombre_proyecto', 'descripcion_proyecto', 'categoria_id', 'logo']).issubset(proyectos_df.columns):
            raise ValueError("La hoja 'Proyectos' debe contener las columnas 'nombre_proyecto', 'descripcion_proyecto', 'categoria_id' y 'logo'")
        
        resultados = {"ferias": 0, "categorias": 0, "proyectos": 0}
        
        # Carpeta base para la ruta de logos
        logo_base_path = "assets/logos/"
        imagen_base_path ="assets/imagen/"
        
        for _, row in ferias_df.iterrows():
            feria = Feria(
                numero_feria=row["numero_feria"],
                anno=row["año"],
                lugar=row["lugar"]
            )
            db.add(feria)
            db.commit()
            db.refresh(feria)
            resultados["ferias"] += 1
            
            # Procesar la hoja "Categorias" asociadas a la feria
            feria_categorias_df = categorias_df[categorias_df["feria_id"] == row["id"]]
            for _, cat_row in feria_categorias_df.iterrows():
                # Procesar imagen para la categoría
                imagen_filename = cat_row.get("imagen")
                imagen_path = f"{imagen_base_path}{imagen_filename}" if imagen_filename else None
                
                categoria = Categoria(
                    nombre_categoria=cat_row["nombre_categoria"],
                    descripcion_categoria=cat_row["descripcion_categoria"],
                    imagen=imagen_path,
                    feria_id=feria.id
                )
                db.add(categoria)
                db.commit()
                db.refresh(categoria)
                resultados["categorias"] += 1
                
                categoria_proyectos_df = proyectos_df[proyectos_df["categoria_id"] == cat_row["id"]]
                for _, proj_row in categoria_proyectos_df.iterrows():
                    logo_filename = proj_row.get("logo")
                    logo_path = f"{logo_base_path}{logo_filename}" if logo_filename else None
                    
                    proyecto = Proyecto(
                        nombre_proyecto=proj_row["nombre_proyecto"],
                        descripcion_proyecto=proj_row.get("descripcion_proyecto"),
                        categoria_id=categoria.id,
                        logo=logo_path  # Guardar la ruta relativa al logo en la base de datos
                    )
                    db.add(proyecto)
                    db.commit()
                    resultados["proyectos"] += 1
        
        return resultados
    
    except Exception as e:
        raise ValueError(f"Error al procesar el archivo: {str(e)}")




def autenticar_admin(db: Session, admin_data: AdminAuth):
    admin = (
        db.query(Admin)
        .filter(Admin.email == admin_data.email, Admin.password == admin_data.password)
        .first()
    )
    if not admin:
        raise HTTPException(status_code=401, detail="Credenciales de administrador incorrectas")
    admin_info = {
        "id_admin": admin.id,
        "nombre": admin.nombre,
        "apellido": admin.apellido,
        "email": admin.email,
        "password": admin.password
    }
    return JSONResponse(content={ "votante": admin_info, "statusCode": 200})

def generar_pdf_resultados(db: Session) -> BytesIO:
    # Obtener los datos
    datos = obtener_datos_combinados(db)
    buffer = BytesIO()
    
    # Crear el documento PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Resultados de Votación")

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Resultados de Votación")

    # Agregar los datos de votación por categoría
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, "Votos por Categoría:")
    y_position = 700
    for categoria in datos["votos_categorias"]:
        pdf.drawString(70, y_position, f"{categoria['nombre_categoria']}: {categoria['votos']} votos")
        y_position -= 20

    # Agregar los datos de votación por proyecto
    pdf.drawString(50, y_position - 20, "Votos por Proyecto:")
    y_position -= 40
    for proyecto in datos["votos_proyectos"]:
        pdf.drawString(70, y_position, f"{proyecto['nombre_proyecto']} - {proyecto['nombre_categoria']}: {proyecto['votos']} votos")
        y_position -= 20

    # Agregar el porcentaje de participación
    pdf.drawString(50, y_position - 20, f"Porcentaje de Participación: {datos['porcentaje_participacion']}%")

    # Finalizar el documento PDF
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    return buffer


def generar_excel_resultados(db: Session) -> BytesIO:
    # Obtener los datos combinados
    datos = obtener_datos_combinados(db)
    buffer = BytesIO()
    
    # Crear un ExcelWriter para manejar múltiples hojas
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Crear DataFrame para categorías
        categorias_df = pd.DataFrame(datos["votos_categorias"])
        categorias_df.rename(columns={'nombre_categoria': 'Categoría', 'votos': 'Votos'}, inplace=True)
        categorias_df.to_excel(writer, sheet_name='Votos por Categoría', index=False)
        
        # Crear DataFrame para proyectos
        proyectos_df = pd.DataFrame(datos["votos_proyectos"])
        proyectos_df.rename(columns={'nombre_proyecto': 'Proyecto', 'nombre_categoria': 'Categoría', 'votos': 'Votos'}, inplace=True)
        proyectos_df.to_excel(writer, sheet_name='Votos por Proyecto', index=False)
        
        # Crear hoja para el porcentaje de participación
        participacion_df = pd.DataFrame({
            "Porcentaje de Participación": [f"{datos['porcentaje_participacion']}%"]
        })
        participacion_df.to_excel(writer, sheet_name='Resumen', index=False)
    
    buffer.seek(0)
    return buffer
