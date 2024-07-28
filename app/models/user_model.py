from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func
from ..db import db_config

Base = db_config.Base

# Crear modelo de usuario
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(50), unique=True, index=True)
  email = Column(String(100), unique=True, index=True)
  full_name = Column(String(100))
  password = Column(String(100))
  is_active = Column(Boolean, default=True)
  created_at = Column(TIMESTAMP, server_default=func.now())
  updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
