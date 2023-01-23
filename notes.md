## Why do we need Schema
- Its hard to get all the values from the body.
- The client can send whatever data they want.
- The data isn't getting validated.
- We ultimately want to force the client to send data in a schema that we expect.

## what is Schema
How we define the data should look like.
* We can create Schema's using pydantic which comes pre-installed with `pip install fastapi[api]`.
We can use pydantic to define what our Schema should look like.

```python
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    Post: str
    publish: bool = True  # Optional argument, default to True
    rating: Optional[int] = None  # Optional argument, default to None


```
Pydantic performs self validation, which means if we do not supply the arguments then it will automatically throw an error and if value is passed then it will perform type checking, throw error's if found.

