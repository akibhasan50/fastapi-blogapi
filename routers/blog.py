from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas
import models
import database
from typing import List
from repository import blog
router = APIRouter(prefix="/blog",
                   tags=["blog"])


@router.post("/",  status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):

    return blog.create_blog(request, db)


@router.get("/",  response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(database.get_db)):
    return blog.get_all_blog(db)


@router.get("/{id}",  status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def single_blog(id: int,  db: Session = Depends(database.get_db)):
    return blog.single_blog(id, db)


@router.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def blog_delete(id: int, db: Session = Depends(database.get_db)):

    return blog.delete_blog(id, db)


@router.put("/{id}",  status_code=status.HTTP_202_ACCEPTED)
def blog_edit(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):

    return blog.edit_blog(id, request, db)
