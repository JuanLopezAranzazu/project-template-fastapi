from pydantic import BaseModel
from typing import Optional

# Token schema
class Token(BaseModel):
  access_token: str
  token_type: str

# TokenData schema
class TokenData(BaseModel):
  id: Optional[str] = None
