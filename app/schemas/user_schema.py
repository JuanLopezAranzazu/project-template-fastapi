from pydantic import BaseModel
from datetime import datetime

# UserBase schema
class UserBase(BaseModel):
  full_name: str
  username: str
  email: str
  password: str

# User schema
class User(UserBase):
  id: int
  is_active: bool
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

