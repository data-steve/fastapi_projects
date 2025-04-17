from app import schemas
from jose import jwt
from config import settings
import pytest

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

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', '123', 403),
    ('voldemort@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403), 
    (None, 'wrongpassword', 403),
    ('voldemort', None, 403)
])
def test_incorrect_login( client, email, password, status_code):
    res = client.post("/login", data = {"username":email, "password":password})
    
    assert res.status_code==status_code
    # assert res.json().get("detail") == 'Invalid Credentials'
    