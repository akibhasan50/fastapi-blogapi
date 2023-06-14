from fastapi import FastAPI, Depends
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


@app.post("/blog",tags=["blog"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    #  new_blog = models.Blog(**request.dist())
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog",tags=["blog"])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",tags=["blog"])
def single_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
