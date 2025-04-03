from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils
from .oauth2 import create_access_token

router = APIRouter(
    tags=['Authentication'] 
) 

@router.post('/login')  
def login(user_credentials: OAuth2PasswordRequestForm = Depends()
          , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email==user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'Invalid Credentials' )
        
    password_verification = utils.verify(user_credentials.password, 
                                         user.password)
    
    if not password_verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'Invalid Credentials' )
        
    access_token = create_access_token(data = {"user_id":user.id})
        
    return {'access_token': access_token, "token_type": "bearer"}