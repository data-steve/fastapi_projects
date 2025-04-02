from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 

my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": i} for i in range(4)]

# print(my_posts)

def find_post(id): 
    for l in my_posts:
        if l['id'] == id:
            return l


@app.get("/")
def root():
    return {'message':'all good'}

@app.get("/posts")  
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(2,100_000_000) 
    my_posts.append(post_dict)
    return {"da ta": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    return {"data": find_post(id)}