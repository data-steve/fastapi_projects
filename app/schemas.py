from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    class Config:
        from_attributes = True
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None