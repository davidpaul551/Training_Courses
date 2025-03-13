from fastapi import HTTPException ,status
from sqlalchemy.orm.session import Session

from db.hash import Hash
from db.models import  db_users_table,db_article_table
from exceptions import StoryException
from schemas import UserBase,ArticleBase,ArticleDisplay


def create_article(db:Session,request :ArticleBase):
    if request.content.startswith('Once upon'):
        raise StoryException("No Stories please")
    new_article = db_article_table(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_article(db:Session,id:int):
    article= db.query(db_article_table).filter(db_article_table.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with {id} not found")
    return article


def delete_article(db:Session,id:int):
    delete_ar_row=db.query(db_article_table).filter(db_article_table.id==id).first()
    db.delete(delete_ar_row)
    db.commit()
    return {"message": f"Article with ID {id} deleted successfully"}
    