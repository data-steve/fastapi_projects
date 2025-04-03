from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# ALGO
# EXPIRATION TIME

SECRET_KEY = '915e8a88c9aeeba07945a944accfed00ce96307203dc883eb14a7969eb82f0dc'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt