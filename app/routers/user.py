from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import utils, models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserResponse) 
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'user {id} was not found' )
    return user


@router.get("/", response_model=List[schemas.UserResponse])  
# @router.get("/") 
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    
    return users