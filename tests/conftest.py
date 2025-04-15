from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from app.database import get_db, Base
import pytest

from fastapi.testclient import TestClient

from app.main import app 

# had to run `PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -c "CREATE DATABASE fastapi_test;"` to create fastapi_test database
SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture( )
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture
def test_user(client):
    user_data = {"email":"voldemort@gmail.com", "password":"123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user