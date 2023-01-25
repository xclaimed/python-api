from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi import status, HTTPException

app = FastAPI()

# Variable to store all the posts created by the user temporally in the memory rather than in database.
# For testing purposes.
all_posts = [
    {
        "title": "Title of post 1",
        "content": "Content of post 1",
        "id": 1
    },
    {
        "title": "Title of post 2",
        "content": "Content of post 2",
        "id": 2
    }
]


# Creating a Schema using pydantic
# step 1 import BaseModel from pydantic
# Step 2 define the input fields.
class Post(BaseModel):
    """
    This is a schema class that will represent how our post schema should look like.
    This class is going to extend BaseModel class(from pydantic import BaseModel).
    This takes cares of all the validation.
    if some field is empty or not mentioned or some value supplied does not it automatically throws the error.
    """
    title: str
    content: str
    publish: bool = True  # This is an optional field
    rating: Optional[int] = None


def find_post(post_id):
    """Function to find the post in our database using ID."""
    for post in all_posts:
        if post["id"] == post_id:
            return post


def find_post_index(post_id):
    """Delete the post with the required ID."""
    # find the post in the array that has the required ID and return the index of the post.
    for index, post in enumerate(all_posts):
        print(index, post)
        if post['id'] == post_id:
            print("we found that")
            return index, post

    return None, None


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
    return {"data": all_posts}


@app.post("/posts", status_code=status.HTTP_404_NOT_FOUND)
def create_posts(payload: Post):
    """
    Create a new post and save that to the database. Return the newly created post.
    """
    post_dict = payload.dict()  # This is a pydantic object, so this way we can create this into a python dict object.
    post_dict["id"] = len(all_posts) + 1  # Giving the new post a new and unique ID.
    all_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """
    Returns the post with the specified post_id. The post_id should be a valid integer.
    'post_id' is also referred as path parameters.
    'post_id: int' auto converts the post_id to int, and we don't have to manually do that.
    It also performs the validation i.e. if some invalid integers are passed then it will automatically throw an error.
    "value is not a valid integer"
    """
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{post_id}' was not found!"
        )
    return {f"Post": post}


# deleting a post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """
    Delete a post.
    """
    index, post = find_post_index(post_id)
    print(f"index: {index}, post: {post}")
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: '{post_id}' was not found."
        )
    all_posts.pop(index)

    # When we delete something we don't generally return something.
    # return {
    #     "details": {
    #         "message": f"Post with ID '{post_id}' was successfully deleted",
    #         "Post": post
    #     }
    # }

