from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils

router = APIRouter(
    tags=['Authentication']
) 

@router.post('/login')  
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email==user_credentials.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'Invalid Credentials' )
        
    password_verification = utils.verify(user_credentials.password, 
                                         user.password)
    
    if not password_verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'Invalid Credentials' )
        
    return {'example':'token'}