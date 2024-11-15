from src.models.models import Votante, Voto, Admin, Categoria, Proyecto
from src.config.db import SessionLocal
import random
import string

def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def load_initial_data():
    db = SessionLocal()

    try:
        # Crear 1 administrador
        admin = Admin(
            rut=12345678,
            dv='9',
            nombre="Admin",
            apellido="Principal",
            email="admin@ejemplo.com",
            password="123123"
        )
        db.add(admin)
        db.commit()

        # Crear 10 votantes
        votantes = []
        for i in range(10):
            votante = Votante(
                rut=10000000 + i,
                dv=str((i % 9) + 1),
                nombre=f"Votante{i+1}",
                apellido=f"Apellido{i+1}",
                email=f"votante{i+1}@ejemplo.com",
                codigo_acceso=generate_unique_code(),
                estado_codigo=True
            )
            votantes.append(votante)
        db.bulk_save_objects(votantes)
        db.commit()

        # Verificar que los votantes fueron creados
        votantes_db = db.query(Votante).all()
        if len(votantes_db) < 10:
            raise Exception("No se crearon todos los votantes")

        # Obtener las categorías y proyectos de la base de datos
        categorias = db.query(Categoria).all()
        proyectos = db.query(Proyecto).all()

        # Verificar que existan categorías y proyectos en la base de datos
        if not categorias or not proyectos:
            raise Exception("No se encontraron categorías o proyectos en la base de datos")

        # Crear votos, asegurando que cada votante vote solo una vez por categoría
        votos_creados = 0
        for votante in votantes_db:
            for categoria in categorias:
                # Obtener un proyecto aleatorio de esta categoría
                proyectos_categoria = [p for p in proyectos if p.categoria_id == categoria.id]
                if proyectos_categoria:
                    proyecto = random.choice(proyectos_categoria)
                    # Crear el voto
                    voto = Voto(
                        votante_id=votante.id,
                        proyecto_id=proyecto.id
                    )
                    db.add(voto)
                    votos_creados += 1
                    # Commit individual para cada voto
                    db.commit()
                # Limitar el número de votos a 25
                if votos_creados >= 25:
                    break
            if votos_creados >= 25:
                break

        print(f"Datos iniciales cargados correctamente. Se crearon {votos_creados} votos.")
    
    except Exception as e:
        db.rollback()
        print(f"Error al cargar datos iniciales: {str(e)}")
    
    finally:
        db.close()




