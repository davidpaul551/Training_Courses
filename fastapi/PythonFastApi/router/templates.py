from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from custom_log import log

router = APIRouter(
    prefix="/templates",
    tags=["templates"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/products/{id}", response_class=HTMLResponse)
def get_product(id:str,request:Request,bt:BackgroundTasks):
    bt.add_task(log_template_call,f"Template read for product id {id}")
    return templates.TemplateResponse(
        "product.html",
        {
            "request":request,
            "id":id
        }
    )




def log_template_call(message:str):
    log("MyAPI",message)