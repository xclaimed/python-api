- [Schema](#schema)
  - [Why do we need Schema](#why-do-we-need-schema)
  - [what is Schema](#what-is-schema)
- [CRUD](#crud)
  - [Certain best practices we need to follow:](#certain-best-practices-we-need-to-follow)
- [path parameter](#path-parameter)
    - [Returning 404 if post is not found and changing the error message](#returning-404-if-post-is-not-found-and-changing-the-error-message)
  - [Restructuring our code](#restructuring-our-code)
- [Database](#database)
  - [SQL](#sql)
    - [Tables](#tables)
    - [Postgres DataTypes](#postgres-datatypes)
    - [Primary Key](#primary-key)
- [Constraints](#constraints)
  - [Unique Constraints](#unique-constraints)
  - [Null Constraints](#null-constraints)
  - [Postgres datatypes](#postgres-datatypes-1)
  - [First Query](#first-query)
- [Integrating with Postgres](#integrating-with-postgres)
  - [Connecting with database](#connecting-with-database)
    - [Getting post from the database](#getting-post-from-the-database)
    - [Creating new post](#creating-new-post)
    - [Getting post from database](#getting-post-from-database)
    - [Deleting post from database](#deleting-post-from-database)
    - [Updating a post](#updating-a-post)
- [Object Relational Mapper (ORM)](#object-relational-mapper-orm)
    - [Get Posts](#get-posts)
    - [Updating Creating post](#updating-creating-post)
    - [Updating getting posts](#updating-getting-posts)
- [Updating deleting posts](#updating-deleting-posts)
    - [Updating a post](#updating-a-post-1)
  - [Pydantic vs ORM models](#pydantic-vs-orm-models)
    - [Creating more Schemas](#creating-more-schemas)
    - [Creating response schema](#creating-response-schema)
- [Authentication and Users](#authentication-and-users)
  - [Adding a user](#adding-a-user)
    - [Creating a table for user](#creating-a-table-for-user)
    - [Schema for create\_user.](#schema-for-create_user)
    - [Creating a New path operation for creating a user](#creating-a-new-path-operation-for-creating-a-user)
    - [Hashing user password](#hashing-user-password)
  - [Routers](#routers)
  - [Authentication](#authentication)

# Schema
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
Type hints is a feature of Python that allows you to explicitly declare the data type of variable when declaring it.

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
| -------- | --------- | ---------- | ----------------------- |
| Create   | POST      | /posts     | @app.post("/posts")     |
| Read     | GET       | /posts/:id | @app.get("/posts/{id}") |
| Read     | GET       | /post      | @app.get("/posts")      |
| Update   | PUT/PATCH | /post/:id  | @app.put("/posts/{id}") |
| Delete   | DELETE    | /post/:id  | @app.delete(/post/{id}) |


## Certain best practices we need to follow:
- Naming the urls and the paths for each operation there is a standard convention, Since we are working with social media posts, so it makes sense to name all the urls or all the paths with `/posts`. It's important to use plural form of post, it is a standard convention for apis. If we were working with users then the path to be used should be `/users`.

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
We don't work or interact with database directly. Instead, we make use of a software referred to as a **Database Management System(DBMS)**.\
DBMS is going to sit in the middle. When we want to perform an operation on a database we're going to send that request to a database management system, that database management system is then actually going to perform that operation, and then it's going to send the result back to us.

There are Two major branches of Database:
* **Relational Databases**
  * MYSQL
  * POSTGRESQL
  * ORACLE
  * SQL SERVER \
Relational databases are usually sql-base databases.

* **NoSQL**
  * MongoDB
  * DynamoDB
  * ORACLE
  * SQL SERVER

## SQL
SQL is a Structured Query Language(SQL) used to communicate with the DBMS.

* When we install postgres, we can carve out multiple separate databases.

### Tables
A table represent a subject or event in an application. e.g. table for registered users, table for reviews and table for all the products you have. Therefore, a table represent different subject or event in an application. **All these tables are going to form some sort of relationship, that's why it's referred to as a relational database**.

When it comes to a table it has **Columns and Rows**.
* Each **Column** represents a different attribute.
* Each **Row** represents a different entry in the table.

![img.png](meta/imgs/tables_rows.png)

### Postgres DataTypes
Databases have datatypes just like any programming language. \
This is important because when you create a column within a table you need to specify what kind of datatype you want to use.

![img.png](meta/imgs/postgres_datatypes.png)
![img_1.png](meta/imgs/postgres_datatypes_2.png)

### Primary Key
When we create a table we have to specify something called a **Primary Key**. **Primary Key** is a column or group of columns that uniquely identifies each row in a table. Each table can have one and only one primary key. Primary key can span multiple columns.
The Primary key does not have to be the ID Column always.

# Constraints
***
## Unique Constraints
A Unique constraint can be applied to any column to make sure every record has a unique value for that column. and if someone tries to add a same value then it will throw an error.

## Null Constraints
By default, when adding a new entry to a database, any column can be left blank. When a column is left blank, it has a `NULL` value.

If you need column to be properly filled in to create a new record, a `NOT NULL` constraint can be added to the column to ensure that the column is never left blank.

## Postgres datatypes
- integer
- serial(It increments the value by 1 automatically, and we don't have to manually suplly value.)
- character varying
- timestamp with time zone
- timestamp without time zone

[Datatypes in Postgres](https://www.postgresql.org/docs/current/datatype.html, "Postgres Documentation")


## First Query
```sql
`SELECT * from products;`
/*This command gives us every single row in the products table. Here ( SELECT ) means to select, ( * ) means to select every column(attribute). We can filter out columns based on our requirements and ( from products(table name)) this gives us all the rows in the table.*/

`SELECT name, id from products;`
-- This command only returns the name and id column. It is important to note that the column returned are in the same order as the query.

`SELECT name AS producut_name, id AS product_id FROM products;`
--- Renaming the columns

`SELECT * FROM products WHERE id = 10;`
--- Filtering result based on some filters.

`SELECT * FROM products WHERE price >= 50;`
--- Operators in sql

`SELECT * FROM products WHERE inventory != 0;`
`SELECT * FROM products WHERE inventory <> 0;`
--- not equal

SELECT * FROM products WHERE inventory <> 0 AND price >= 30;
-- Multiple operators

SELECT * FROM products WHERE id = 1 OR id = 2 OR id = 3;
SELECT * FROM products WHERE id IN (1, 2, 3);
--- Returns any matched 

SELECT * FROM products WHERE name LIKE 'TV%';
--- Match anythings that starts with TV and have anything afterwords. We can actually pass a regex expresion here. '%e' - everything that ends with e.

SELECT * FROM products WHERE NOT LIKE 'TV%';
--- Match everything that does not starts with 'TV'. '%en%' will match anything that contains en. 

SELECT * FROM products ORDER BY price DESC;
--- Order result in descending order based on price. Ascending order is default.

SELECT * FROM products ORDER BY inventory DESC, price;
--- When there is a tie like in inventory the value was 0, then we can order them based on another column.

SELECT * FROM products ORDER BY ID LIMIT 5 OFFSET 5;
--- Limits the result and can offset(remove the first 5 results).

INSERT INTO products (name, price) VALUES ('ps5', 1000);
-- Add Item to the table.

INSERT INTO products (name, price) VALUES ('ssd', 250), ('hdd', 100) RETURNING *;
-- BY default INSERT query only returns the codes not the data. We can filter the column also by ID, price replacint *.

DELETE FROM products WHERE id = 10;
DELETE FROM products WHERE id = 111 RETURNING *;


UPDATE products SET name='myname', price=222 WHERE id = 22 RETURNING *;
-- update the row.

UPDATE products SET name='myname', price=222 WHERE id > 22 RETURNING *;
-- Updating multiple values.
```
==IMP==
- In sql captilzation does not matters. `select * FROM products` == `SELECT * from products`
- Best practice is to Uppercase the sql keywords and lowercase the user provided information. It helps to easily differentiate between sql keywords and user inputs in really long sql queries.
- Use code when you have to match a string or text or character varying.


# Integrating with Postgres
When it comes to working with postgres database within a python application, we're going to need a postgres driver. There are many different library, we are going to use pysycopg2
`pip install psycopg2`

## Connecting with database
```py
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

```

### Getting post from the database
```python
@app.get("/posts", status_code=status.HTTP_404_NOT_FOUND)
def get_all_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.findall()
    return {'data': posts}
```

### Creating new post
You never want to do any string interpolation and then pass in the values Post directly into the database query. Instead what we want to do is, we are going to parametize or sanatize all the data that we put into the sql statement. So that we are not vulerable to sql injection.
```python
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_new_post(payload: Post):
   cursor.execute(
    """ INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING *""",
    (payload.title, payload.content, payload.publish)
   )
    new_post = cursor.fetchone()

    conn.commit()  # To save data in the database.
    return {'data', new_post}

```

### Getting post from database
```python
@app.post('posts/{post_id}')
def get_post(post_id: int):
    # here we validated that the post_id is always an integer.

    cursor.execute("""SELECT * FROM posts WHERE ID = %s)""", (str(post_id),)) # , for any issue
    # here we converted the post_id back to string becuase it expects id to be a string.

    post = cursor.findone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found"
        )
    return {'post_details': post}
```

### Deleting post from database
```python
@app.delete('posts/{post_id}')
def delete_post(post_id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s""", (str(post_id),)
    )
    deleted_post = cursor.fetchone()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {post_id} was not found.'
        )

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

### Updating a post
```python
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
```

# Object Relational Mapper (ORM)
There are couple of different ways of interacting with the database. One way is using raw sql queries and other is ORM.

ORM is a layer of abstraction that sits between the database and the application. 

We can perform all database operations through tradational python code. No more SQL! So some of the benefits is that we don't actually have to work with sql anymore so instead of using raw sql what we'll do is we'll actually use standard python code calling various functions and method that ultimately translate into sql themselves.

![ORM](meta/imgs/orm.png)
![ORM](meta/imgs/orm2.png)

- SQLALCHEMY
Sqlalchemy is one of the most popular python ORMs.


```python
# models.py
# Here we are going to store all our models.
# Every model represents a table in our database
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = 'posts' 

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```

```python
# database.py

# Setting up connection with the database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = 'postgresql//<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1324@localhost/python-api'

# Creating a engine, engine is responsible for sqlalchemy to connect to a postgres database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database we have to make a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We have to define our base class, So all of the model we define to actually create our tables in postgres, they're going to be extending this base class.
Base = declarative_base()
```

```python
# models.py

# Here we are going to store all our models.
# Every model represents a table in our database
from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False
```

```python
# main.py

# Creating our declared models
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import session
from fastapi import Depends

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Get Posts
```python
# here, the session object is responsible for talking with the databases, here we created a function (get_db) to get a connection to our database or session to our database, so every time we get a request we're going to get a session, then be able to send sql statements and finally after the request is done then close the session.
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post
```

### Updating Creating post 
```python
# main.py
@app.post('/posts')
def create_posts(post: Post, db: Session = Depends(get_db)):
    # sql method
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.publish))
    # new_post = cursor.fetchone()

    # conn.commit()  # saving the changes in the databse.

    # sqlalchemy method
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=content.published
    # )
    # above line is can also be written as
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refrest(new_post)

    return {'data': new_post}
```

### Updating getting posts
```python
@app.get('/posts/{post_id}')
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail='Post with id: {post_id} was not found')

    return {'post': post}
```

# Updating deleting posts
```python
@app.delete('/posts/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # sql
      # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id))
    # )
    # deleted_post = cursor.fetchone()

    # sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
            details=f'post with id: {id} was not found'
            )
    db.delete(synchronize_session=False))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

### Updating a post
```python

@app.put('/posts/{id}')
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    # sql
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload.title, payload.content, payload.published, str(post_id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    # sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == post_id) 
    post = post_query.filter()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_POST_NOT_FOUND,
            detail=f'Post with id: {post_id} was not found.'
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'post': post_query.first()}

```

## Pydantic vs ORM models
Pydantic
![Schema Model(Pydantic)](meta/imgs/schema_models.png)

Sqlalchemy Model
![sqlalchemy Model](meta/imgs/sqlalchemy.png)


### Creating more Schemas
Every different operation can have a different schema.

```python
# This will be our base class for all the schemas to inherit from.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass
```

### Creating response schema
We can define how the request should look like and we can also define how our response should look like.

Creating a response schema
```python
# schemas.py
class Response(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    # Pydantic response models requires the response to be in a dict.
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes)
    class Config:
        orm_mode = True


# Same as above
class Response(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
```
[Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode)


# Authentication and Users

## Adding a user
### Creating a table for user
```python
# models.py
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)  # unique = True will prevent user from registering twice with one email
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```

### Schema for create_user.
```python
# schemas.py
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    # email: str
    # We can also check for valid emails, with the email-validator that is included with the pydantic module.
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

```

### Creating a New path operation for creating a user
```python
# main.py
@app.post('/users', status=status.HTTP_201_CREATED)
def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
```

### Hashing user password
So when it comes to working with password in databases we always hash the password, we never store the actual password in our database.
[FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#install-passlib)

`pip install "passlib[bcrypt]"`

```python
# main.py
from passlib.context import CryptoContext

# passlib config
# This is telling passlib to use bcrypt algorithm
pwd_context = CryptoContext(schemas=["bcrypt"], deprecated="auto")

@app.post('/users', status=status.HTTP_201_CREATED)
def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user_data.password)
    user_data.password = hashed_password
    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
```                                                                  

Get user details with id
```py
# main.py
@app.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist"
            )

    return user
```

## Routers
We are going to see routers, to split up all of our path operations so that we can organize our code.

```py
# user.py, post.py
from fastapi import APIRouter

router = APIRouter(
    # Adding prefix so we dont have to enter the same url repeatedly
    prefix='/users', # now we replace /users with 
    tag=['User'] # to group the documentation
)

# replace all app. pathoperations with router.
router.get('/{id}')

# main.py
from .routers import post, user

app.include_router(post.router)
app.include_router(user.router)
```

# Authentication
There are two main ways to tackle authentication:
- Session Based Authentication
The idea behind session is that we store something on our backend server to track whether a user logged in.
- JWT Token Authentication
The idea behind JWT token authentication is that it's stateless, i.e. there's nothing on our backend. JWT is stored on our client that acutally keeps tracks of whether user is logged in or not. It is stored in the frontend on our client and keep tracks of whether user is logged in or not.

![JWT Token Authentication](meta/imgs/jwt_intro..png)
Here the api does not track anything, there's no information stored on the api, Instead the client hold on the token and he provides it to us and we verify the token.
## What JWT token is and what components make up Token?
![JWT Components](meta/imgs/JWT_components.png)
JWT token is bunch of cryptic characters but they are not encrypted. Token is make up of 3 inidvidual pieces.
- Header
Header includes metadata about the token. We are going to hash(sign) the token so we need to specify the algorithm to use, default is 'HS256', so we've included that in the header.
- Payload
Payload is up to you. You can send abosolutely no payload or you can send any piece of information that you want within the payload. We should be carefull what we put in the payload because token itself is not encrypted. Generally put the user_id into the token.
- Signature
Signature is a combination of 3 things. Header, Payload and our special password that we keep on our api. So we take all these inforamtion and pass it into the signing algorithm which is 'HS256' and it is going to return a signature. And this signature is important becuase we are going to use this to determine if the token in valid.

**Anyone can see the data of token, anyone can change the data of token they just cannot generate brand new signature because they don't have access to our secret.**

```py
# utils.py
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# schemas.py
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# auth.py

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def user_login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
            )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

```

## Creating JWT Token
`pip install "python-jose[cryptography]"`

```py
# oauth2.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

# there will be 3 pieces of information we need to provide to create token
# SECRET_KEY
# algorithm - 
# expiration time - if we return a token with no expiration time that means user is logged in forever

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    data = payload.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token
```

** We are going to make a small change when it comes to retrieving the user's credential.**
Instead of using our Schema we are going to user built in fastapi utility.

```py
# routers/auth.py
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

@router.post('/login')
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # we have to send data in form-data format, it will not accept raw data.
    # Now user_credential will contain two fields only (username, password)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
            )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    # Create Token
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
```

## Validating the token

```python
# oauth2.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')

# Secret_key
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Algorithm
ALGORITHM = "HS256"

# Expiration date
# expiration date dictates how long a user should be logged in after they perform a login operation
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()  # Creating copy so that orignal data don't get manipulated
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get('user_id') # type: ignore  

        if id is None:
            raise credentials_exception
        
        # validating the schema 
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

# We can pass this as a dependency to any of our path operations.
# it is going to take the token from the request automatically, extract the id
# verify the token by calling verify_access_token, fetch the user and add it as a 
# parameter into our path operation function.
def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f'Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
    )
    return verify_access_token(token, credentials_exception)
```

## Protecting routes
```python
from .. import oauth

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    '''
    This function(oauth2.get_current_user) is now going to be a dependency. This forces the user to be logged in before they can actually create post.
    When they hit this endpoint this function is called this function then calls verify_access_token by passing in the tag in the token which comes from the user.
    Then we first decode the token, extract the id. If no id then we throw an error, then we validate the schema and then return the extracted token data.
    '''
    pass
```


# Relationship
How we create relationship in relational database?
We create an extra column(user_id) in our database(post). Then we are going to set up a foreign key. A foreign key is how we tell sql that this column is connected to another table. Here we specify two things, first the table(user table) that is should be connected to and then we specify what specific column(id column) it should use from that table.

whatever user creates this post we just embed the id of the user.
![One To Many Relationship](meta/imgs/one_to_many_relationship.png)

```py
# models.py

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # changed

# schemas.py
# Sending back the responses.
class PostResponse(PostBase):
    id: int
    created_at: datetime
    author_id: int
    
    class Config:
        orm_mode = True


# routes/post.py
# add user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = model.Post(author_id=current_user.id, **payload)

# delete user
@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.PostResponse)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.Post = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found.",
        )
    
    if post.author_id != current_user.id: # changed
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action"
        )
    post_query.delete(synchornize_session=False)
```

# SQLalchemy Relationship
This relationship is not a foreign key, id does nothing in the database whatsoever, but it tells sqlalchemy to automatically fetch some piece of information based off the relationship. This has no effect on our database.
```py
# models.py
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    author = relationship('User')  # we pass the sqlalchemy class, this is going to return class of another model
    # So this creates another property automatically for our post. so when we retrieve a post it's going to return a author property. SO it's going to fetch the user based off the author_id and return that for us.

# schemas.py
# Sending back the responses.
class PostResponse(PostBase):
    id: int
    created_at: datetime
    author_id: int
    author: UserResponse    
    class Config:
        orm_mode = True

```

# Query Parameters
Query Parameters are optional key value pairs that appears to the right of the question mark. These query parameters allows to filter the result of a request like show post with 100 likes, show post that are created within 2 hours.

```py
# post.py
@router.get('/', response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ''):
    posts = db.query(models.Post).filter(models.Post.contains(search).limit(limit).offset(skip)).all()
    return posts
```
spacing in url `?search=robin%20hood`.

# Environment Variable
.env file is going to contain all of our environment vairables. So we can set much easier just by having a file do all the work. In production we're not going to use this, in production we are going to actually set these on our machines.
```py
# .env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=1324
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTS=30

# config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str = '5432'
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # telling pydantic to import it from .env file
    class Config:
        env_file = '.env'


settings = Settings()
```