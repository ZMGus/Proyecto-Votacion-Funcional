from src.config.db import Base
from sqlalchemy import Integer, Boolean, String, DateTime, ForeignKey, Time, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime

class Votante(Base):
    __tablename__ = 'votantes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rut: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False) 
    dv: Mapped[str] = mapped_column(String, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    codigo_acceso: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    estado_codigo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    votos: Mapped[List["Voto"]] = relationship("Voto", back_populates="votante")

    
class Feria(Base):
    __tablename__ = 'ferias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero_feria: Mapped[int] = mapped_column(Integer, nullable=False)
    anno: Mapped[int] = mapped_column(Integer, nullable=False)
    lugar: Mapped[str] = mapped_column(String, nullable=False)

    categorias: Mapped[List["Categoria"]] = relationship("Categoria", back_populates="feria")

class Categoria(Base):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_categoria: Mapped[str] = mapped_column(String, nullable=False)
    descripcion_categoria: Mapped[Optional[str]] = mapped_column(String)
    imagen: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    feria_id: Mapped[int] = mapped_column(Integer, ForeignKey('ferias.id'))


    feria: Mapped["Feria"] = relationship("Feria", back_populates="categorias")
    proyectos: Mapped[List["Proyecto"]] = relationship("Proyecto", back_populates="categoria")
   

    
class Proyecto(Base):
    __tablename__ = 'proyectos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_proyecto: Mapped[str] = mapped_column(String, nullable=False)
    descripcion_proyecto: Mapped[Optional[str]] = mapped_column(String)
    nombre_pre_empresa: Mapped[Optional[str]] = mapped_column(String)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey('categorias.id'))
    logo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="proyectos")
    votos: Mapped[List["Voto"]] = relationship("Voto", back_populates="proyecto")
    
class Voto(Base):
    __tablename__ = 'votos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    votante_id: Mapped[int] = mapped_column(Integer, ForeignKey('votantes.id'), nullable=False)
    proyecto_id: Mapped[int] = mapped_column(Integer, ForeignKey('proyectos.id'), nullable=False)
    fecha_voto: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    votante: Mapped["Votante"] = relationship("Votante", back_populates="votos")
    proyecto: Mapped["Proyecto"] = relationship("Proyecto", back_populates="votos")

    __table_args__ = (
        UniqueConstraint('votante_id', 'proyecto_id', name='unique_voto_votante_proyecto'),
    )
    
class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True,nullable=False)
