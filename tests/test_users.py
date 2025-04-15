from app import schemas
from .database import client, session
import pytest
from jose import jwt
from config import settings


@pytest.fixture
def test_user(client):
    user_data = {"email":"voldemort@gmail.com", "password":"123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_create_users(client):
    res = client.post("/users/", json={"email":"voldemort@gmail.com", "password":"123"})
    new_user = schemas.UserResponse(**res.json()) 
    assert new_user.email == "voldemort@gmail.com"
    assert res.status_code==201
    

def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code==200