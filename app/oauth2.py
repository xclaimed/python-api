from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
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
ACCESS_TOKEN_EXPIRE_MINUTES = 60


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
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f'Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
    )
    payload =  verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == payload.id).first()
    return user

