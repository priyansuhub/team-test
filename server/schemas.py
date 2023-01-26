from typing import Optional
from pydantic import BaseModel, EmailStr

class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None