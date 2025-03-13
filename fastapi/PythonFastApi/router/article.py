from typing import List
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas import UserBase, UserDisplay,ArticleBase,ArticleDisplay,ArticleResponse
from db.database import get_db
from db import db_article_logic

from auth.oauth2 import oauth2_schema,get_current_user

router = APIRouter(
    prefix='/article',
    tags=['article']
)

@router.post('/',response_model=ArticleDisplay)
def create_article(request:ArticleBase,db:Session=Depends(get_db)):
    return db_article_logic.create_article(db,request)


# @router.get('/{id}',response_model=ArticleDisplay)
# def get_article(id:int,db:Session=Depends(get_db),token:str = Depends(oauth2_schema)):
#     return db_article_logic.get_article(db,id)

# depends on the authorized user not token
@router.get('/{id}', response_model=ArticleResponse)
def get_article(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    article = db_article_logic.get_article(db, id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return {
        "data": article,
        "Current_user": current_user
    }

@router.post('/{id}/delete',response_model=dict)
def delete_article(id:int,db:Session=Depends(get_db)):
    return db_article_logic.delete_article(db,id)