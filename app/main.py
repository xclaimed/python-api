import time
import psycopg2
from typing import Optional, List
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# # connecting the database
# while True:  # retry if connection failed
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='python-api',
#             user='postgres',
#             password='1324',
#             cursor_factory=RealDictCursor
#         )

#         cursor = conn.cursor()  # we are going to use this to execute our sql statements.
#         print("Database connection was succesfull!")

#         break  # if connection is established

#     except Exception as error:
#         print("Connection to the database failed!")
#         print("Error: ", error)
#         time.sleep(10)  # Sleep for 10 seconds before trying again.


# In this library, these functions are called Path Operations(routes)
@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)