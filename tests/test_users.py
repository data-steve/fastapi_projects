from app import schemas
from jose import jwt
from config import settings


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
    
def test_incorrect_login(test_user, client):
    res = client.post("/login", data = {"username":test_user['email'], "password":"yada"})
    
    assert res.status_code==403
    assert res.json().get("detail") == 'Invalid Credentials'
    