from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import SessionLocal, get_db
from db import models
from db.hash import Hash
from auth import oauth2

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):#Authorization form which contain the username and pass inputs
    user = db.query(models.db_users_table).filter(models.db_users_table.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password")
    
    access_token = oauth2.create_access_token(data={'sub':user.username})
    
    return {
        "access_token": access_token,
        "token_type":"bearer",
        "user_Id":user.id,
        "username":user.username
    }