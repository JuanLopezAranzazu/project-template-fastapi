from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import global_config
from ..schemas import token_schema
from ..db import db_config
from ..models import user_model

settings = global_config.settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Funcion para verificar el token de acceso
def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    if id is None:
      raise credentials_exception
    token_data = token_schema.TokenData(id=id)
  except JWTError:
    raise credentials_exception

  return token_data


# Funcion para obtener el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db_config.get_db)):
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=f"Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(user_model.User).filter(user_model.User.id == token.id).first()

    return user
