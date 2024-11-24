from pydantic import BaseModel,EmailStr, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default value if user does not provide value
    # rating : Optional [int] = None # allows value to be optional

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post # can combine response model
    votes : int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr #email validator
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(... , le =1, ge =-1) #allow number between -1 and 1