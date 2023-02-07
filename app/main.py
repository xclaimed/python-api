import time
import psycopg2
from typing import Optional
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# connecting the database
while True:  # retry if connection failed
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='python-api',
            user='postgres',
            password='1324',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()  # we are going to use this to execute our sql statements.
        print("Database connection was succesfull!")

        break  # if connection is established

    except Exception as error:
        print("Connection to the database failed!")
        print("Error: ", error)
        time.sleep(10)  # Sleep for 10 seconds before trying again.


# In this library, these functions are called Path Operations(routes)
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    """
    Function to get all the posts of the current user.
    Returns:
    """
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db)):
    """
    Create a new post and save that to the database. Return the newly created post.
    """
    new_post = models.Post(**payload.dict())  # dict unpacking

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
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
    return {"post_detail": post}


# deleting a post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a post.
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: '{post_id}' was not found."
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    # When we delete something we don't generally return something.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post_data: schemas.CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found."
        )

    post_query.update(post_data.dict(), synchronize_session=False)
    
    db.commit()

    return { "post": post_query.first()}
