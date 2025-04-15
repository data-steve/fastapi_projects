from fastapi.testclient import TestClient
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

from app.main import app 

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Hello!"
    assert res.status_code ==200


def test_create_users():
    res = client.post("/users/", json={"email":"voldemort@gmail.com", "password":"123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "voldemort@gmail.com"
    assert res.status_code==201
    
    
# def test_get_users():
#     res = client.get("/users/", json={"email":"elaine@gmail.com", "password":"123"})
#     print(res)
    
#     client.get()