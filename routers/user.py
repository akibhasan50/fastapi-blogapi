from fastapi import APIRouter,Depends,status, HTTPException
from utils.hashing import Hash
from database import get_db
from sqlalchemy.orm import Session
import schemas,models,database

router = APIRouter(prefix="/user",
                   tags=["user"])
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.becrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    all_user = db.query(models.User).all()
    return all_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_single_user(id: int, db: Session = Depends(get_db)):
    user_by_id = db.query(models.User).filter(models.User.id == id).first()
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with  {id} not found")
    return user_by_id
