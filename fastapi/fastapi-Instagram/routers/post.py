from typing import List
from fastapi import APIRouter , Depends,HTTPException ,status , UploadFile, File
from schemas import PostBase , PostDisplay
from sqlalchemy.orm.session import Session
from db.database_creation import get_db
from db import db_Post_logic
import random
import string
import shutil
from schemas import UserAuth
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute','relative']

@router.post('',response_model=PostDisplay)
def create_New_Post(request:PostBase,db:Session = Depends(get_db),current_user :UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take values 'absolute' or 'relative' ")
    return db_Post_logic.create_Post(db,request)

@router.get('/all' , response_model=List[PostDisplay])
def get_all_posts(db:Session=Depends(get_db)):
    return  db_Post_logic.get_all_post(db)


@router.get('/post/{id}',response_model=PostDisplay)
def get_Post_By_ID(id:int, db:Session = Depends(get_db)):
    return db_Post_logic.get_Post_Id(id,db)

@router.post('/image')
def upload_Image(image:UploadFile=File(...),current_user :UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f"_{rand_str}"
    filename = ".".join([image.filename.rsplit(".", 1)[0] + new, image.filename.rsplit(".", 1)[1]])
    path = f"images/{filename}"

    with open(path,"w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)

    return {'filename':path}


@router.get('/delete/{id}')
def delete_Post(id:int,db:Session = Depends(get_db),current_user:UserAuth = Depends(get_current_user)):
    return db_Post_logic.delete_The_Post(db,id,current_user.id)
