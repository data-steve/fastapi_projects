from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 


# import psycopg
# from psycopg.rows import dict_row
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try: 
        conn = psycopg2.connect("host=localhost dbname=fastapi user=postgres password=postgres",
                            #    row_factory=dict_row
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection wa s successful!")
        break
    except KeyboardInterrupt: 
        print("Stopped by user")
    except Exception as error:
        print(f"Error connecting to database:\n\tError = {error}")
        time.sleep(2)
        
my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": (i-2)} for i in range(10,2,-1)]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # id: int
 


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


# @app.get('/sqlalchemy')  
# def test_post( db: Session = Depends(get_db) ):
#     posts = db.query(models.Post).all()
    
#     return {'data':posts}


@app.get("/posts")  
def get_posts(db: Session = Depends(get_db)):
    # raw sql via psycog version
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # raw sql via psycog version
    # cursor.execute("""INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,  (post.title, post.content, post.published)) 
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s  """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'id {id} was not found' )
    return {"data": post} 


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # # delete via find index and pop
    # idx = find_index_post(id) 
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'post id={id} does not exist')
        
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put('/posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail= f'post id={id} does not exist')
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return {'data': post_query.first()}