import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar las variables ocultas del archivo .env
load_dotenv()

# ==========================================
# CONFIGURACIÓN MySQL
# ==========================================
MYSQL_URL = os.getenv("MYSQL_URL")
if not MYSQL_URL:
    print("❌ Error: No se encontró MYSQL_URL en el archivo .env")
else:
    try:
        engine = create_engine(MYSQL_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        print("✅ Conexión preparada para MySQL local")
    except Exception as e:
        print(f"❌ Error al configurar MySQL: {e}")

def get_mysql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# CONFIGURACIÓN MongoDB Atlas
# ==========================================
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "turutamed_db")

mongo_client = None
mongo_db = None

if not MONGO_URI:
    print("❌ Error: No se encontró MONGO_URI en el archivo .env")
else:
    try:
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client[MONGO_DB_NAME]
        # Esto fuerza a que Mongo verifique la conexión (un 'ping')
        mongo_client.admin.command('ping')
        print(f"✅ Conexión exitosa a MongoDB Atlas (Base de datos: {MONGO_DB_NAME})")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB Atlas: Verifica tu usuario/contraseña o tu conexión a internet.\nDetalle: {e}")