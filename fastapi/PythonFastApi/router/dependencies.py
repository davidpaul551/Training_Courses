from fastapi import APIRouter, Depends,Request
from custom_log import log

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(log)]
    
)

def convert_parameters(request:Request,seperator:str):
    query_parameters=[]
    for key, value in request.query_params.items():
        query_parameters.append(f"{key}{seperator}{value}")
    return query_parameters

def convert_headers(request:Request,query=Depends(convert_parameters)):
    out_headers=[]
    for key,value in request.headers.items():
        out_headers.append(f"{key} -- {value}")
    return {
        "headers":out_headers,
        "query parameters":query
    }



@router.get("/")
def get_items(headers = Depends(convert_headers)):
    return {
        "items":['a','b','c'],
        "headers":headers
    }


class Account:
    def __init__(self, name :str, email:str):
        self.name = name
        self.email = email


def get_account(name: str, email: str):
    return Account(name, email)

@router.post('/user')
def create_user(name:str,email:str,password:str,account : Account= Depends(Account)):
    return {
        "name":account.name,
        "email":account.email
    }









