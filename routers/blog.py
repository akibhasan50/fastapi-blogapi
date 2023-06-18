from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas
import models
import database
from typing import List

router = APIRouter(prefix="/blog",
                   tags=["blog"])


@router.post("/",  status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    #  new_blog = models.Blog(**request.dist())
    new_blog = models.Blog(title=request.title,
                           body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/",  response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}",  status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def single_blog(id: int,  db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Blog with  {id} not found"))
    return blog


@router.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def blog_delete(id: int, db: Session = Depends(database.get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Blog with  {id} not found"))
    blog.delete()
    db.commit()
    return "done"


@router.put("/{id}",  status_code=status.HTTP_202_ACCEPTED)
def blog_edit(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Blog with  {id} not found"))
    blog.update(
        {'title': request.title, 'body': request.body})
    db.commit()
    return "updated"
