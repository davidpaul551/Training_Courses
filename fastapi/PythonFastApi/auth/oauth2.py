from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2AuthorizationCodeBearer , OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException,status
from sqlalchemy.orm.session import Session 

from db.database import get_db
from db import db_user_Logic

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt




def get_current_user(token:str = Depends(oauth2_schema),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the data",
        headers={"WWW_Authenticate":"Bearer"}
    )
    try:
        payload =jwt.decode(token, SECRET_KEY,ALGORITHM)
        username:str= payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user_Logic.get_one_user_by_username(db,username)
    if user is None:
        raise credentials_exception
    return user
