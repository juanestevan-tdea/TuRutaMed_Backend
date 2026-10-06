from pydantic import BaseModel, EmailStr
from datetime import datetime

# Esto es lo que PEDIMOS al usuario cuando se registra
class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr  # Valida que sea un correo real con '@'
    contrasena: str
    rol: str = "Usuario_Regular"  # Por defecto todos son regulares

# Esto es lo que DEVOLVEMOS al usuario (jamás devolvemos la contraseña)
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True  # Permite traducir de la Base de Datos a la API
        
# Lo que pedimos para el Login
class UsuarioLogin(BaseModel):
    email: EmailStr
    contrasena: str

# Lo que devolvemos si el login es exitoso
class Token(BaseModel):
    access_token: str
    token_type: str