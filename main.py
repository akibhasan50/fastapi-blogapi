from fastapi import FastAPI, Path
import schemas

app = FastAPI()

@app.post("/blog")
def create(request: schemas.Blog):
    return request
