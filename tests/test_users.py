from fastapi.testclient import TestClient
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from app.database import get_db, Base

from app.main import app 

# had to run `PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE fastapi_test;"` to create fastapi_test database
SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


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