from typing import List
from pydantic import BaseModel

#Article inside userDisplay
class Article(BaseModel):
    title:str
    content:str
    published:bool
    class Config():
        orm_mode=True


#Request Body
class UserBase(BaseModel):
    username:str
    email: str
    password:str

#Response Body
class UserDisplay(BaseModel):
    username:str
    email:str
    items:List[Article]=[]
    class Config():
        orm_mode=True #converts the data to the specified data format here


#User inside article display
class User(BaseModel):
    id:int
    username:str



class ArticleBase(BaseModel):
    title:str
    content:str
    published:bool
    creator_id:int


class ArticleDisplay(BaseModel):
    title:str
    content:str
    published:bool
    userRel:User
    class Config():
        orm_mode = True


class ArticleResponse(BaseModel):
    data: ArticleDisplay
    Current_user: UserDisplay
