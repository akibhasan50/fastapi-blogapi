from fastapi import FastAPI, Depends, status, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import schemas
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Blog API')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", tags=["blog"], status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    #  new_blog = models.Blog(**request.dist())
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", tags=["blog"])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", tags=["blog"], status_code=status.HTTP_200_OK)
def single_blog(id: int,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Blog with  {id} not found"))
    return blog


@app.delete("/blog/{id}", tags=["blog"], status_code=status.HTTP_204_NO_CONTENT)
def blog_delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    return "done"


@app.put("/blog/{id}", tags=["blog"], status_code=status.HTTP_202_ACCEPTED)
def blog_edit(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
   
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Blog with  {id} not found"))
    blog.update(
        {'title': request.title, 'body': request.body})
    db.commit()
    return "updated"
