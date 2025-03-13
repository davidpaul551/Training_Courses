from schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import db_Comments_table
from datetime import datetime 
from fastapi import HTTPException, status
from schemas import CommentBase

def create_Comm(db:Session , request:CommentBase):
    new_comm = db_Comments_table(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.now()
    )
    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)
    return new_comm

def get_all_Comms(db:Session , post_id:int):
    return db.query(db_Comments_table).filter(db_Comments_table.id == post_id).all()
