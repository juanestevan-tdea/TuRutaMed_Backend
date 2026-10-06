from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_mysql_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioRegistro, UsuarioRespuesta, UsuarioLogin, Token
from app.core.seguridad import obtener_hash_contrasena, verificar_contrasena, crear_token_acceso

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# 1. RUTA DE REGISTRO (La que ya teníamos)
@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: UsuarioRegistro, db: Session = Depends(get_mysql_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este correo electrónico ya está registrado.")
    
    clave_segura = obtener_hash_contrasena(usuario_in.contrasena)
    nuevo_usuario = Usuario(
        nombre=usuario_in.nombre,
        email=usuario_in.email,
        contrasena_encriptada=clave_segura,
        rol=usuario_in.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# 2. NUEVA RUTA DE LOGIN
@router.post("/login", response_model=Token)
def iniciar_sesion(usuario_in: UsuarioLogin, db: Session = Depends(get_mysql_db)):
    
    # A. Buscamos al usuario en la BD por su email
    usuario_bd = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if not usuario_bd:
        # Si no existe, error 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    
    # B. Comparamos la contraseña plana con el hash raro de la BD
    if not verificar_contrasena(usuario_in.contrasena, usuario_bd.contrasena_encriptada):
        # Si no cuadra, error 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    
    # C. Si todo está perfecto, creamos el Pasaporte (JWT)
    # Metemos su email y su rol dentro del token para saber quién es cuando vuelva
    token = crear_token_acceso(data={"sub": usuario_bd.email, "rol": usuario_bd.rol})
    
    # D. Le entregamos el pasaporte
    return {"access_token": token, "token_type": "bearer"}