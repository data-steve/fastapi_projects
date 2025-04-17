from sqlite3 import connect
from app import schemas
import json
import pytest 

def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # print(json.dumps(res.json(), indent=4),'\n')
    # print(test_posts)
    def _validate(post):
        return schemas.PostVote(**post)
    
    posts_validated = list(map(_validate, res.json()))
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code ==200
    # assert posts_validated[0].Post.id == test_posts[0].id
    
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{100}")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
     
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostVote(**res.json())
    # print(res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("title 1", "content 1", True),
    ("title 2", "content 2", False),
    ("title 3", "content 3", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    
    res = authorized_client.post('/posts/', json = { "title":title, "content": content, "published":published} )
    new_post = schemas.PostResponse(**res.json())
    # print(new_post)
    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published 
    assert new_post.owner_id == test_user['id']



@pytest.mark.parametrize("title, content", [
    ("title 1", "content 1"),
    ("title 2", "content 2"),
    ("title 3", "content 3")
])
def test_create_post_default_published_true(authorized_client, test_user, title, content):
    
    res = authorized_client.post('/posts/', json = { "title":title, "content": content} )
    new_post = schemas.PostResponse(**res.json())
    # print(new_post)
    assert res.status_code == 201
    assert new_post.published 
    

def test_unauthorized_user_create_post_default_published_true(client):
    res = client.post('/posts/', json = { "title":'hi', "content": 'bye'} )
    # print(new_post)
    assert res.status_code == 401
    

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'
    
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    # print(res.status_code)
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user):
    res = authorized_client.delete(f'/posts/{10000}')
    assert res.status_code == 404


def test_delete_other_users_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401
    # assert res.json()['detail'] == 'Not authenticated'


def test_update_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json={"title": "totally new title", "content": "totally new title"})
    # The line `print(res.status_code)` is used to print out the status code of the response received
    # after making a request in the test case `test_update_post_success`. This helps in debugging and
    # verifying that the status code returned by the API endpoint matches the expected status code.
    # print(res.status_code)
    assert res.status_code == 202
    
# def test