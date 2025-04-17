from app import schemas, models
import pytest 

# test_vote_not_authorized
# test_vote_post_does_not_exist
# test_vote_user_does_not_exist
# test_vote_up_success     xxx 
# test_vote_down_success   xxx
# test_vote_up_fail
# test_vote_down_fail

@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_fail_post_does_not_exist(authorized_client):
    data = {'post_id':6, 'dir':1}
    res = authorized_client.post('/vote/', json=data)
    assert 'does not exist' in res.json()['detail']
    assert res.status_code ==404
    

def test_vote_up_success(authorized_client, test_posts):
    data = {'post_id':test_posts[1].id, 'dir':1}
    res = authorized_client.post('/vote/', json=data)
    assert 'added' in res.json()['message']
    assert res.status_code ==201


def test_vote_up_fail_already_voted(authorized_client, test_posts, test_vote):
    data = {'post_id':test_posts[3].id, 'dir':1}
    res2 = authorized_client.post('/vote/', json=data)
    # print(res2.json(), res2.status_code)
    assert 'already voted' in res2.json()['detail']
    assert res2.status_code ==409
    
def test_delete_vote_fail_vote_does_not_exist(authorized_client, test_posts):
    data = {'post_id':test_posts[1].id, 'dir':0}
    res = authorized_client.post('/vote/', json=data)
    # print(res.json(), res.status_code)
    assert 'not yet voted' in res.json()['detail']
    assert res.status_code ==404
    
def test_delete_vote_success(authorized_client, test_posts, test_vote):
    
    data_down = {'post_id':test_posts[3].id, 'dir':0}
    res2 = authorized_client.post('/vote/', json=data_down)
    assert 'deleted' in res2.json()['message']
    assert res2.status_code ==201
    

def test_vote_not_authorized(client):
    res = client.post("/vote/")
    assert res.status_code == 401
    