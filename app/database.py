from typing import Any

import certifi
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# ==========================================
# CONFIGURACIÓN MySQL
# ==========================================
MYSQL_URL = settings.mysql_url
try:
    engine = create_engine(MYSQL_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("✅ Conexión preparada para MySQL local")
except Exception as e:  # noqa: BLE001
    print(f"❌ Error al configurar MySQL: {e}")


def get_mysql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# CONFIGURACIÓN MongoDB
# ==========================================
MONGO_URI = settings.mongo_url
MONGO_DB_NAME = settings.mongo_db_name

mongo_client: Any = None
mongo_db: Any = None


def get_mongo_db():
    """Retorna la instancia de la base de datos MongoDB (o None si no está conectada)."""
    return mongo_db


try:
    use_tls = "mongodb+srv://" in MONGO_URI or "tls=true" in MONGO_URI.lower()
    if use_tls:
        mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    else:
        mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB_NAME]
    mongo_client.admin.command("ping")
    print(f"✅ Conexión exitosa a MongoDB (Base de datos: {MONGO_DB_NAME})")
except Exception as e:  # noqa: BLE001
    mongo_client = None
    mongo_db = None
    print(
        "❌ Error conectando a MongoDB: Verifica tu usuario/contraseña o tu "
        f"conexión a internet.\nDetalle: {e}"
    )
