from fastapi import HTTPException,status
from schemas import PostBase,PostDisplay
from sqlalchemy.orm.session import Session
import datetime
from db.database_creation import database
from db.models import db_PostTable



def create_post(db:Session , request:PostBase):
    new_post = db_PostTable(
        image_url = request.image_url,
        title = request.title,
        content = request.content,
        creator = request.creator,
        timestamp=datetime.datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get all posts
def get_all_Posts(db:Session):
    return db.query(db_PostTable).all()

#Delete
def delete_post(id:int , db:Session):
    post_item = db.query(db_PostTable).filter(db_PostTable.id==id).first()
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    db.delete(post_item)
    db.commit()
    return f"Post deleted with id {id}"

