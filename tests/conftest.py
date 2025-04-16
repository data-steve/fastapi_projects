from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from config import settings
from app.database import get_db, Base
import pytest
from app import models

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


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title":"1st title",
         "content":"1st contetn",
         "owner_id": test_user['id']},
        {"title":"2nd title",
         "content":"2nd stuff",
         "owner_id": test_user['id']},
        {"title":"3rd title",
         "content":"3rd nknnk",
         "owner_id": test_user['id']}
        # {"title":"4th title",        # default api lmits to 3 so testing only 3
        #  "content":"4th nkn0nk",
        #  "owner_id": test_user['id']}
    ]
    
    def _create_post_model(post):
        return models.Post(**post)
    
    post_map = map(_create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts