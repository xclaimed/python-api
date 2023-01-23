from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


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


# In this library, these functions are called Path Operations
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_posts")
def create_posts(payload: Post):
    print(payload, type(payload))
    payload.dict()  # This is an pydantic object, so this way we can create this into a python dict object.
    return {"data": "new post"}
