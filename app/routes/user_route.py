from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from argon2 import PasswordHasher
from ..models import user_model
from ..schemas import user_schema
from ..db import db_config

# Ruta para usuarios

NAME_ROUTE = "users"

router = APIRouter(
  prefix=f"/{NAME_ROUTE}",
  tags=[NAME_ROUTE]
)

# Para encriptar la contraseña
ph = PasswordHasher()

@router.get("/", response_model=List[user_schema.User])
async def get_users(db: Session = Depends(db_config.get_db)):
  users = db.query(user_model.User).all()
  return users

@router.get("/{user_id}", response_model=user_schema.User)
async def get_user(user_id: int, db: Session = Depends(db_config.get_db)):
  user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id {user_id} not found"
    )
  return user

@router.post("/", response_model=user_schema.User)
async def create_user(user: user_schema.UserBase, db: Session = Depends(db_config.get_db)):
  user_db = db.query(user_model.User).filter(user_model.User.username == user.username).first()
  
  if user_db:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already registered"
    )

  new_user = user_model.User(
    full_name=user.full_name,
    username=user.username,
    email=user.email,
    password=ph.hash(user.password)
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(user_id: int, user: user_schema.UserBase, db: Session = Depends(db_config.get_db)):
  user_db = db.query(user_model.User).filter(user_model.User.id == user_id).first()

  # Validar si el usuario existe
  if user_db is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id {user_id} not found"
    )

  user_db.full_name = user.full_name
  user_db.username = user.username
  user_db.email = user.email
  user_db.password = ph.hash(user.password)

  db.commit()
  db.refresh(user_db)
  return user_db

@router.delete("/{user_id}", response_model=user_schema.User)
async def delete_user(user_id: int, db: Session = Depends(db_config.get_db)):
  user = db.query(user_model.User).filter(user_model.User.id == user_id).first()

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"User with id {user_id} not found"
    )

  db.delete(user)
  db.commit()
  return user

