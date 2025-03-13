from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username : str
    email : str
    password : str


class UserDisplay(BaseModel):
    username :str
    email : str
    class Config():
        orm_mode = True


class PostBase(BaseModel):
    image_url :str
    image_url_type:str
    caption:str
    creator_id :int
    
#For Post Display
class User(BaseModel):
    username:str
    class Config():
        orm_mode=True

# Comments for Post Display
class Comments(BaseModel):
    text:str
    username:str
    timestamp : datetime
    class Config():
        orm_mode = True
    
class PostDisplay(BaseModel):
    id:int
    image_url:str
    image_url_type:str
    caption:str
    timestamp:datetime
    comments : List[Comments]
    user:User
    class Config():
        orm_mode = True


class UserAuth(BaseModel):
    id:int
    username:str
    email:str




class CommentBase(BaseModel):
    username:str
    text:str
    post_id:int


