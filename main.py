from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 

my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": (i-2)} for i in range(10,2,-1)]

# print(my_posts)

def find_post(id): 
    for l in my_posts:
        if l['id'] == id:
            return l

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i


@app.get("/")
def root():
    return {'message':'all good'}

@app.get("/posts")  
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(2,100_000_000) 
    my_posts.append(post_dict)
    return {"data": post_dict}
 
 
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'id {id} was not found' )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error':f'id {id} was not found'}
    return {"post_detail": post  }


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete via find index and pop
    idx = find_index_post(id)
    print(idx)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'post id={id} does not exist')
    # print(idx)
    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put('/posts/{id}')
def update_post(id: int, payload: dict = Body(...)):
    idx = find_index_post(id)
    post = my_posts.pop(idx)
    # post['title'] = "I made you better"
    if payload is not None:
        for k,v in payload.items():
            post[k]=v
    my_posts.append(post)
    return {'message': f'post id {id} has been updated'}