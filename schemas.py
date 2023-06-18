from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    title: str
    body: str
    user_id: int

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog] = []

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    id:int
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True
