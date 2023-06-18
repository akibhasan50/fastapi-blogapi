from fastapi import APIRouter, Depends, status, HTTPException
from utils.hashing import Hash
from database import get_db
from sqlalchemy.orm import Session
import schemas
import models
import database
from repository import user
router = APIRouter(prefix="/user",
                   tags=["user"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    return user.create_user(request, db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return user.get_all_user(db)



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_single_user(id: int, db: Session = Depends(get_db)):

    return user.get_user(id, db)
