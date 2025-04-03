
from datetime import datetime
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # id: int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id : int
    created_at : datetime
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str