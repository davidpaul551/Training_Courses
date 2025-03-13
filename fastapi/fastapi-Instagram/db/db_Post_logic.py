from schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import db_Post_table
import datetime
from fastapi import HTTPException, status

def create_Post(db:Session ,request:PostBase ):
    new_post = db_Post_table(
         image_url = request.image_url,
        image_url_type= request.image_url_type,
        caption = request.caption,
        timestamp = datetime.datetime.now(),
        user_id= request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_Post_Id(id : int ,db:Session):
    return db.query(db_Post_table).filter(db_Post_table.id == id).first()

def get_all_post(db:Session):
    return db.query(db_Post_table).all()



def delete_The_Post(db:Session , id:int,user_id:int):
    post = db.query(db_Post_table).filter(db_Post_table.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with id {id} is not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only post creator can delete the post")
    db.delete(post)
    db.commit()
    return "Ok"

