from fastapi import FastAPI
from database import engine
import models
from routers import blog
from routers import user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Blog API')

app.include_router(blog.router)
app.include_router(user.router)


