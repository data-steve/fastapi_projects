from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 
    
    class Config:
        from_attributes = True 

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserResponse
    class Config:
        from_attributes = True 
        
        
class PostVote(BaseModel):
    Post : PostResponse
    votes : int
    
    class Config:
        from_attributes = True 
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
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
    
class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]