from pydantic import BaseModel


# class Post(BaseModel):
#     """
#     This is a schema class that will represent how our post schema should look like.
#     This class is going to extend BaseModel class(from pydantic import BaseModel).
#     This takes cares of all the validation.
#     if some field is empty or not mentioned or some value supplied does not it automatically throws the error.
#     Creating a Schema using pydantic
#     step 1 import BaseModel from pydantic
#     Step 2 define the input fields.
#     """
#     title: str
#     content: str
#     published: bool = True  # This is an optional field
#     # rating: Optional[int] = None


# This will be our base class for all the schemas to inherit from.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

