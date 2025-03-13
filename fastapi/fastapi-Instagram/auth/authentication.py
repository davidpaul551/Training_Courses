from fastapi import APIRouter, Depends , HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from db.database_creation import get_db
from sqlalchemy.orm.session import Session
from db.models import db_User_table
from db.hashing import Hash
from auth.oauth2 import create_access_token



router = APIRouter(
    tags = ['authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(db_User_table).filter(db_User_table.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
    if not Hash.verify(user.password , request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Incorrect Password")
    access_token = create_access_token(data={'username':user.username})
    
    
    return {
        'access_token': access_token,
        'token_type':"bearer",
        'user_id':user.id,
        'username':user.username
    }