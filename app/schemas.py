

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
    title:  str
    content: str
    published: bool =True


class PostCreate(PostBase): #class postcreate extending PostBase class or inheriting 
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

#Creating Response Model for receiving or send back exact data you want
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #for response model to work because pydantic works with dict
    #for sqlalchemy to work we pass orm_mode = True where pydantic ignores dict and convert to orm
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


#Creating response model for create user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


#create schemas for access_token and token type and match accordingly
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #to represent only 0 or 1 (conint, le=1 is less than or equal to 1)
