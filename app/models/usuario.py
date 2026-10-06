from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # Así se llamará la tabla en MySQL

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contrasena_encriptada = Column(String(255), nullable=False)
    
    # Aquí controlamos los Roles (RBAC)
    rol = Column(String(50), default="Usuario_Regular") 
    
    # Para saber si la cuenta está activa o baneada
    activo = Column(Boolean, default=True)
    
    # Guarda la fecha y hora exacta en la que se registró
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())