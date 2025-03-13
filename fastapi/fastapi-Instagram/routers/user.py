from fastapi import APIRouter ,Depends
from schemas import UserDisplay,UserBase
from sqlalchemy.orm.session import Session
from db.database_creation import get_db
from db.db_user_logic import create_user

router = APIRouter(
    prefix="/user",
    tags=['user']
)



@router.post('', response_model=UserDisplay)
def create_User(request:UserBase , db:Session = Depends(get_db)):
    return create_user(db,request)