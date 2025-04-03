from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # id: int

class PostCreate(PostBase):
    pass