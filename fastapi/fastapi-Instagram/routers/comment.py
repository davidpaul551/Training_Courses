from fastapi import APIRouter
from fastapi import APIRouter ,Depends
from schemas import CommentBase ,UserAuth
from sqlalchemy.orm.session import Session
from db.database_creation import get_db
from db.db_comments_logic import create_Comm , get_all_Comms
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@router.get('/all/{post_id}')
def all_Comments(post_id:int,db:Session = Depends(get_db)):
    return get_all_Comms(db,post_id)


@router.post('')
def create_Comment(request:CommentBase,db:Session = Depends(get_db), current_user : UserAuth = Depends(get_current_user)):
    return create_Comm(db,request)
    