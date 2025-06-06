from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import schemas, models, oauth2
 
router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostVote])  
# @router.get("/") 
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] = ""):
        # raw sql via psycog version
        # cursor.execute("""SELECT * FROM posts """)
        # posts = cursor.fetchall() 
    # print(limit) 
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post
                       , func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # raw sql via psycog version
    # cursor.execute("""INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,  (post.title, post.content, post.published)) 
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s  """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post
                       , func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print('Current user',current_user)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'id {id} was not found' )
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # delete via find index and pop
    # idx = find_index_post(id) 
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f'post id={id} does not exist')
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put('/{id}', response_model=schemas.PostResponse, status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail= f'post id={id} does not exist')
        
    if post.owner_id != current_user .id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()