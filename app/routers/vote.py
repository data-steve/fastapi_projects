from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2, database
 
router = APIRouter(
    prefix='/vote',
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # check post existence
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {vote.post_id} does not exist.')

    # check if vote pre-exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    vote_status = vote_query.first()

    # handle voting logic
    if vote.dir == 1:
        if vote_status :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on post {vote.post_id}")
        else :
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        if not vote_status:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} has not yet voted on post {vote.post_id}.")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
        return {"message": "successfully deleted vote"}
