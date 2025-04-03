from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto" )


def hash(password: str):
    return pwd_context.hash(password)


# def verify(plain_password: str, hashed_stored_password: str):
#     hashed_plain_password = hash(plain_password) 
#     return hashed_plain_password == hashed_stored_password

def verify(plain_password: str, hashed_stored_password: str):
    return pwd_context.verify(plain_password, hashed_stored_password)