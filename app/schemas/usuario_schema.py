from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Esto es lo que PEDIMOS al usuario cuando se registra
class UsuarioRegistro(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    nombre: str
    email: EmailStr
    contrasena: str = Field(alias="password")
    rol: str = "Usuario_Regular"


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
    model_config = ConfigDict(populate_by_name=True)
    email: EmailStr
    contrasena: str = Field(alias="password")


# Lo que devolvemos si el login es exitoso
class Token(BaseModel):
    access_token: str
    token_type: str
