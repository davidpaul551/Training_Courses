from typing import List
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas import UserBase, UserDisplay
from db.database import get_db
from db import db_user_Logic

router = APIRouter(
    prefix='/user',
    tags=['user']
)

#Create
@router.post('/',response_model=UserDisplay)
def create_user(request: UserBase,db:Session=Depends(get_db)):
    return db_user_Logic.createUser(db,request)

#Read all users

@router.get('/',response_model=List[UserDisplay])
def get_all_users(db:Session=Depends(get_db)):
    return db_user_Logic.get_all_users(db)

# read one user
@router.get('/{id}')
def get_one_user(id:int,db:Session=Depends(get_db)):
    return db_user_Logic.get_one_user(db,id)

@router.get('/{username}')
def get_one_user_by_username(username: str, db: Session = Depends(get_db)):
    return db_user_Logic.get_one_user_by_username(db, username)


#Update

@router.post('/{id}/update')
def update_user(id:int,request:UserBase,db:Session=Depends(get_db)):
    return db_user_Logic.update_user(db,id,request)

#Delete
@router.post('/{id}/delete')
def delete_user(id:int,db:Session=Depends(get_db)):
    return db_user_Logic.delete_user(db,id)

