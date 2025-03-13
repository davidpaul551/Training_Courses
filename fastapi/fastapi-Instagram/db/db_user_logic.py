
from db.models import db_User_table
from schemas import UserBase,UserDisplay
from sqlalchemy.orm.session import Session
from db.hashing import Hash
from fastapi  import HTTPException , status


def create_user(db:Session,request:UserBase):
    new_user = db_User_table(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)  # Hash the password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_Username(db:Session,username:str):
    user = db.query(db_User_table).filter(db_User_table.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"User with username {username} not found")
    return user


