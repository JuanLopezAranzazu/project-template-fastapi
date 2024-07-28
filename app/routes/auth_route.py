from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from ..models import user_model
from ..schemas import user_schema, token_schema
from ..db import db_config
from ..middlewares import oauth2

# Ruta para autenticación

NAME_ROUTE = "auth"

router = APIRouter(
  prefix=f"/{NAME_ROUTE}",
  tags=[NAME_ROUTE]
)

# Para encriptar la contraseña
ph = PasswordHasher()

@router.post("/login", response_model=token_schema.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_config.get_db)):
  user = db.query(user_model.User).filter(user_model.User.username == user_credentials.username).first()
  
  if user is None or not ph.verify(user.password, user_credentials.password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password"
    )
  
  access_token = user_model.create_access_token(data={"user_id": user.id})
  return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=user_schema.User)
async def register(user: user_schema.UserBase, db: Session = Depends(db_config.get_db)):
  user_db = db.query(user_model.User).filter(user_model.User.username == user.username).first()
  
  if user_db:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already registered"
    )
  
  user_db = user_model.User(
    full_name=user.full_name,
    username=user.username,
    email=user.email,
    password=ph.hash(user.password)
  )
  
  db.add(user_db)
  db.commit()
  db.refresh(user_db)
  
  return user_db

@router.get("/me", response_model=user_schema.User)
async def me(current_user: int = Depends(oauth2.get_current_user)):
  return current_user
