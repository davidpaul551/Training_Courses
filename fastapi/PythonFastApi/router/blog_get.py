from fastapi import APIRouter
from fastapi import status,Response,Depends
from enum import Enum
from typing import Optional
from router.blog_post import required_function


router = APIRouter(
    prefix = "/blog",
    tags = ["blog"]
)

# @app.get('/blog/all')
# def get_all_blogs(page,page_size):
#     return {"message":f"All {page_size} blogs on the {page} page"}

@router.get('/all',
         summary="This is a get all blog",
         description="The Api calls are made to be more finite for the get all blogs",
         response_description="The list of all available blogs"
         )
def get_all_blogs(page=1,page_size: Optional[int]=None,required_param:dict = Depends(required_function)):
    return {"message":f"All {page_size} blogs on the {page} page", "requiredParam":required_param}

@router.get('/{id}/comments/{comment_id}',tags=["comment"])
def get_comment(id: int , comment_id : int,valid:bool = True , username: Optional[str]=None):
    """
    Simulates retrieving a comment of a blog
    - **id** mandatory path parameter
    - **comment_id**  mandatory path parameter
    """
    return {"message":f"blog_id {id} , comment_id {comment_id} , valid {valid}, username{username}"}


# @router.get('/all')
# def get_all_blog():
#     return {"message": "all blogs data"}


class BlogType(str,Enum):
    short='short'
    story='story'
    howto='howto'


@router.get('/type/{type}')
def get_blog_type(type: BlogType):
    return {"message":f'Blog Type {type.value}'}

# Status Code
# @app.router('/{id}',status_code=status.HTTP_404_NOT_FOUND)
# def get_blog(id:int):
#     if id > 5:
#         return{"error":f"Blog {id} not found"}
#     else:
#         return {"message":f"blog with id {id}"}
@router.get('/{id}',status_code=status.HTTP_200_OK)
def get_blog(id:int , response:Response):
    if id > 5:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{"error":f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message":f"blog with id {id}"}

