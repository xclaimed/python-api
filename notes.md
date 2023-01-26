## Why do we need Schema
- It's hard to get all the values from the body/payload.
- The client can send whatever data they want.
- The data isn't getting validated.
- We ultimately want to force the client to send data in a schema that we expect.

## what is Schema
How we define the data should look like.
* We can create Schema's using pydantic which comes pre-installed with `pip install fastapi[api]`.
We can use pydantic to define what our Schema should look like.

* <mark>TypeHints</mark>
Type hints is a feature of Python that allows you to explicitly declare the data type of a variable when declaring it.

```python
# Creating a schema class using pydantic
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    Post: str
    publish: bool = True  # Optional argument, default to True
    rating: Optional[int] = None  # Optional argument, default to None


```
Pydantic performs self validation, which means if we do not supply the arguments then it will automatically throw an error and if value is passed then it will perform type checking, throw error's if found.

# CRUD
Crud is an acronym that represents 4 main functions of an application.

| Property | Method    | Endpoint   | Route                   |
|----------|-----------|------------|-------------------------|
| Create   | POST      | /posts     | @app.post("/posts")     |
| Read     | GET       | /posts/:id | @app.get("/posts/{id}"  |
| Read     | GET       | /post      | @app.get("/posts")      |
| Update   | PUT/PATCH | /post/:id  | @app.put("/posts/{id}") |
| Delete   | DELETE    | /post/:id  | @app.delete(/post/{id}) |


## Certain best practices we need to follow:
- Naming the urls and the paths for each operation there is a standard convention, Since we are working with social media posts, so it makes sense to name all the urls or all the paths with `/posts`. It's important to use plural form of post, it is a standard convention for apis. If we were working with users then the path to be use should be `/users`.

In PUT method, all the fields have to be sent for updating the post and in PATCH method we can send just the specific field that we want to change.


# path parameter
```python
@app.get("/posts/{post_id}")
def get_post_by_post_id(post_id):
    pass
```

* The order of the routes matters:

if route **/posts/{post_id}** is placed above the **/posts/latest** then fastapi will never reach the latest route. It will throw an error *'latest cannot be converted into integer'*. This type of errors occurs when we work with **path parameters**.
Solution is to move the route above the post_id because /1 will never match /latest.

### Returning 404 if post is not found and changing the error message
```python
from fastapi import Response, status

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = 404  # here we hardcoded the response.
        # or 
        # here we can find a list of https codes use the most appropriate one.
        response.status_code = status.HTTP_404_NOT_FOUND
        
        # Return a custom message
        return {"message": f"Post with id: '{id}' was not found!!"}
    return {"post_details": post}
```
This was one method of returning an error but this method is little sloppy.
**Instead, we can raise an HTTP exception, built-in exception in fast api where we can pass the specific error code as well as the message, so we don't have to hard code all of that.**

```python
from fastapi import status, HTTPException

def get_post(id):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: `{id} was not found!"
        )
    return {"post_detail": post}
```
* **Changing default status code of a specific path operation.**\
`@app.post("/posts", status_code=status.HTTP_404_NOT_FOUND)`

* FastAPI automatically generates the documentation based off the path operations that you've defined.
To get the documentations visit url/docs, this is going to show you the built-in documentation powered by **Swagger UI**.

There are two type of documentation built in: 
1. Swagger UI
2. Redoc


## Restructuring our code
We are going to move our code to a folder called app, so that's going to store all of our application specific code.

Python has a concept of packages and a package is nothing more than a fancy name for a folder. However, something to properly act as a package, python requires you to create a dummy file, this file is called __init__.py.

# Database
Database is a collection of organized data that can be easily accessed and managed. \
We don't work or interact with database directly. Instead we make use of a software referred to as a **Database Management System(DBMS)**.\
DBMS is going to sit in the middle. When we want to perform an operation on a database we're going to send that request to a database management system, that database management system is then actually going to perform that operation, and then it's going to send the result back to us.

There are Two major branches of Database:
* **Relational Databases**
  * MYSQL
  * POSTGRESQL
  * ORACLE
  * SQL SERVER
Relational databases are usually sql-base databases.

* **NoSQL**
  * MongoDB
  * DynamoDB
  * ORACLE
  * SQL SERVER

## SQL
SQL is a Structured Query Language(SQL) used to communicate with the DBMS.

* When we install postgres, we can carve out multiple separate databases. 