from fastapi import HTTPException ,status
from sqlalchemy.orm.session import Session

from db.hash import Hash
from db.models import  db_users_table
from schemas import UserBase,UserDisplay

def createUser(db:Session,request:UserBase):
    new_user = db_users_table(
        username = request.username,
        email= request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db:Session):
    return db.query(db_users_table).all()


def get_one_user(db, id):
    user = db.query(db_users_table).filter(db_users_table.id == id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found with ID {id}")
    articles = [
        {"title": a.title, "content": a.content, "published": a.published}  # Ensure 'published' is included
        for a in user.articleRel
    ]

    return UserDisplay(
        username=user.username,
        email=user.email,
        items=articles
    )

def get_one_user_by_username(db: Session, username: str):
    user = db.query(db_users_table).filter(db_users_table.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with username {username}"
        )
    
    articles = [
        {"title": a.title, "content": a.content, "published": a.published}  # Ensure 'published' is included
        for a in user.articleRel
    ]

    return UserDisplay(
        username=user.username,
        email=user.email,
        items=articles
    )




def update_user(db:Session ,id :int , request:UserBase):
    updateRow = db.query(db_users_table).filter(db_users_table.id==id).first()
    if not updateRow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    updateRow.update({
        db_users_table.username : request.username,
        db_users_table.email:request.email,
        db_users_table.password:Hash.bcrypt(request.password)
    })
    db.commit()
    return "Ok"


def delete_user(db:Session,id:int):
    deleteRow = db.query(db_users_table).filter(db_users_table.id==id).first()
    db.delete(deleteRow)
    db.commit()
    return "OK"
