from fastapi import status, HTTPException, Depends, APIRouter
from .. import oauth2, schemas, models, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
    )


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(payload: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    # if post does not exist
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {payload.post_id} does not exist'
        )
    # this query returns if the user have already liked the post or not.
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == payload.post_id,
        models.Vote.user_id == current_user.id
    )
    voted = vote_query.first()
    if payload.dir == 1:
        # if dir is 1 create vote
        if voted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {payload.post_id}"
            )
        else:
            # Create vote
            new_vote = models.Vote(
                post_id=payload.post_id,
                user_id=current_user.id
            )
            db.add(new_vote)
            db.commit()
            return {"message": 'Successfully added Vote'}
    else:
        if not voted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Vote does not exist'
            )
        vote_query.delete()
        db.commit()
        return {'message': 'Successfully deleted Vote'}
