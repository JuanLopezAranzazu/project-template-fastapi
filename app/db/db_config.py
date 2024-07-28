from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import global_config

settings = global_config.settings

# Crear URL de conexión a base de datos
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Crear motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base de datos
Base = declarative_base()

# Conexion a base de datos
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Crear tablas en base de datos
def create_tables():
  Base.metadata.create_all(bind=engine)
