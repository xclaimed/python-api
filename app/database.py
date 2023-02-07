from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1324@localhost/python-api'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1324@localhost/fastapi'

# Creating a engine, engine is responsible for sqlalchemy to connect to a postgres database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database we have to make a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We have to define our base class, So all of the model we define to actually create our tables in postgres, they're going to be extending this base class.
Base = declarative_base()

# Dependency
# This function is going to create a session to our database for every request to that specific endpoint and then it's going to close session when it's done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()