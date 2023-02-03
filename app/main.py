import time
import psycopg2
from typing import Optional
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException

app = FastAPI()


class Post(BaseModel):
    """
    This is a schema class that will represent how our post schema should look like.
    This class is going to extend BaseModel class(from pydantic import BaseModel).
    This takes cares of all the validation.
    if some field is empty or not mentioned or some value supplied does not it automatically throws the error.
    Creating a Schema using pydantic
    step 1 import BaseModel from pydantic
    Step 2 define the input fields.
    """
    title: str
    content: str
    publish: bool = True  # This is an optional field
    rating: Optional[int] = None


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
def create_posts(payload: Post):
    """
    Create a new post and save that to the database. Return the newly created post.
    """
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.publish))
    new_post = cursor.fetchone()

    conn.commit()  # saving the changes in the databse.
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Returns the post with the specified post_id. The post_id should be a valid integer.
    'post_id' is also referred as path parameters.
    'post_id: int' auto converts the post_id to int, and we don't have to manually do that.
    It also performs the validation i.e. if some invalid integers are passed then it will automatically throw an error.
    "value is not a valid integer"
    """
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""", (str(post_id))
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{post_id}' was not found!"
        )
    return {"post_detail": post}


# deleting a post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """
    Delete a post.
    """
    cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id))
    )
    deleted_post = cursor.fetchone()
    print(deleted_post)
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: '{post_id}' was not found."
        )
        
        
    conn.commit()
    # When we delete something we don't generally return something.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, payload: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload.title, payload.content, payload.publish, str(post_id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found."
        )

    return {
        "post": updated_post
    }
