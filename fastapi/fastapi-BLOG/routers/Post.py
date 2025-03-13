from fastapi import APIRouter , Depends,File,UploadFile
from schemas import PostBase,PostDisplay
from sqlalchemy.orm.session import Session
from db.database_creation import database
from db import db_Post_Logic
import string , random
import shutil


router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


@router.post("/")
def create_post(request:PostBase,db:Session= Depends(database)):
    return db_Post_Logic.create_post(db,request)


@router.get("/all")
def get_all_posts(db:Session = Depends(database)):
    return db_Post_Logic.get_all_Posts(db)


@router.delete('/{id}')
def delete_post(id:int , db:Session = Depends(database)):
    return db_Post_Logic.delete_post(id,db)



#Add Image
@router.post('/uploadimage')
def upload_image(image:UploadFile = File(...)):
    # letter = string.ascii_letters
    # rand_str = ' '.join(random.choice(letter) for i in range(6))
    # new = f"_{rand_str}."
    # filename = new.join(image.filename.rsplit('.',1))
    path = f'images/{image.filename}'

    with open(path,'w+b') as buffer:
        shutil.copyfileobj(image.file,buffer)
    return{'filename':path}
