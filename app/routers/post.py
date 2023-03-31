from ..database import get_db
from .. import schemas, models, oauth2
from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ''):
    """
    Function to get all the posts of the current user.
    Returns:
    """
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.Post = Depends(oauth2.get_current_user)):
    """
    Create a new post and save that to the database. Return the newly created post.
    """
    new_post = models.Post(author_id=current_user.id, **payload.dict())  # dict unpacking

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.post("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Returns the post with the specified post_id. The post_id should be a valid integer.
    'post_id' is also referred as path parameters.
    'post_id: int' auto converts the post_id to int, and we don't have to manually do that.
    It also performs the validation i.e. if some invalid integers are passed then it will automatically throw an error.
    "value is not a valid integer"
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{post_id}' was not found!"
        )
    return post


# deleting a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.Post = Depends(oauth2.get_current_user)):
    """
    Delete a post.
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: '{post_id}' was not found."
        )

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail=f"Not authorized to perform requested action."
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    # When we delete something we don't generally return something.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post_data: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.Post = Depends(oauth2.get_current_user)):
    """Updating a post"""
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found."
        )
    
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authroized to perform the requested action."
        )

    post_query.update(post_data.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()