from .. import schemas, models, utils
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = '/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    # hashing the password
    hashed = utils.hash(user_data.password)
    user_data.password = hashed
    new_user = models.User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist"
            )

    return user