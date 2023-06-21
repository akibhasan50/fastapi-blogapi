from fastapi import APIRouter, Depends, status, HTTPException
import schemas
import database
from sqlalchemy.orm import Session
import models
from utils.hashing import Hash
from datetime import datetime, timedelta
from JWTtoken import create_access_token

router = APIRouter(
    tags=["authentication"]
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    # generate jwt token
    access_token = create_access_token(
        data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
