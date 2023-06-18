from sqlalchemy.orm import Session
from fastapi import status, HTTPException
import schemas
import models
from utils.hashing import Hash




def create_user(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.becrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session):
    user_by_id = db.query(models.User).filter(models.User.id == id).first()
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with  {id} not found")
    return user_by_id

def get_all_user( db: Session):
    all_user = db.query(models.User).all()
    return all_user
