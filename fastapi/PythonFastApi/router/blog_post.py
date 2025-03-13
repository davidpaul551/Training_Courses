from fastapi import APIRouter, Query , Path , Body
from pydantic import BaseModel
from typing import Optional , List , Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

# class BlogModel(BaseModel):
#     title: str
#     content:str
#     published: Optional[bool]
#     no_comments:int

#Image submodel class

class Image(BaseModel):
    url:str
    alias:str


#Complex Subtypes
class BlogModel(BaseModel):
    title: str
    content:str
    published: Optional[bool]
    no_comments:int
    tags:List[str]=[]
    metadata:Dict[str,str]={"key1":" ","key2":" "}
    image:Image = None

# @router.post('/')
# def create_blog(blog:BlogModel):
#     return blog

# query and path params in request body
@router.post('/new/{id}')
def create_blog(blog:BlogModel , id:int , version : int = 1):
    return {
        'id':id,
        'data':blog,
        'version':version
        }

#parameter metadata
# @router.post('/new/{id}/comment')
# def create_comment(blog:BlogModel,id:int,
#         comment_id:int = Query(None,
#                 title="Id of the comment",
#                 description="This is the description of the id"
#         )
#     ):
#     return {
#         'blog':blog,
#         'id':id,
#         'comment_id':comment_id
#     }

#Add Alias

# @router.post('/new/{id}/comment')
# def create_comment(blog:BlogModel,id:int,
#         comment_id:int = Query(None,
#                 alias='commentID',
#                 deprecated=True
#         )
#     ):
#     return {
#         'blog':blog,
#         'id':id,
#         'comment_id':comment_id
#     }

#Content is optional and send through the request body with default value
# @router.post('/new/{id}/comment')
# def create_comment(blog:BlogModel,id:int,
#         comment_id:int = Query(None,
#                 title="Id of the comment",
#                 description="This is the description of the id",
#                 alias='COMMENTID',
#                 deprecated=True
#         ),
#         content:str = Body('Hi Whats going on')
#     ):
#     return {
#         'blog':blog,
#         'id':id,
#         'comment_id':comment_id,
#         'content':content
#     }


#To make non-optional
@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog:BlogModel,id:int,
        comment_title:str = Query(None,
                title="Title of the comment",
                description="This is the description of the title",
                alias='Title_ID',
                deprecated=True
        ),
        #content:str = Body(...) #make a non optional(require)
        #content:str=Body(...,min_length=5)#Minimunm length of chars
        #content:str=Body(...,min_length=5,max_length=7)#Minimunm length of chars
        content:str=Body(...,min_length=5,max_length=7,regex='^[a-z\s]*$'  #regular expression matching
                         ),
        # v: Optional[List[str]] = Query(None)
        v:Optional[List[str]] = Query(['1.0','3.4']),# provide default values, remove "OPTIONAL" to make non optional
        comment_id : int = Path(gt=5,le=10) # Number validators as (gt,ge-greater than or equal,lt,le-less than or equal)

    ):
    return {
        'blog':blog,
        'id':id,
        'comment_id':comment_id,
        'content':content,
        'version':v
    }





def required_function():
    return{"message":"learning"}








