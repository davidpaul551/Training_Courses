import time
from typing import List, Optional
from fastapi import APIRouter,Header,Cookie,Form
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from custom_log import log


router = APIRouter(
    prefix='/products',
    tags=['products']
)

products =['watch','car','phone']

async def time_consuming_functionality():
    time.sleep(5)
    return "OK"


@router.post('/new')
def create_product(name:str = Form(...)):
    products.append(name)
    return products

#Custom Responses

@router.get('/all')
async def get_all_products():
    log("MyApI","Call to get all products")
    await time_consuming_functionality()
    #return products
    data = " ".join(products)
    response = Response(content=data , media_type="text/plain")
    response.set_cookie(key='test_cookie',value='test-cookie_value')
    return response

# @router.get('/withheader')
# def get_product_Header(response:Response,custom_header:Optional[str]=Header(None)):
#     return products

@router.get('/withheader')
def get_product_Header(response:Response,
                       custom_header:Optional[List[str]]=Header(None),
                       test_cookie:Optional[str]=Cookie(None)):
     if custom_header:
        response.headers["custom_response_header"]= ", ".join(custom_header)
        return {
            "data":products,
            "custom_header":custom_header,
            "my cookie":test_cookie
        }

@router.get("/{id}",responses={
    200:{
        "content":{
            "text/html":{
               "example": "<div>Product</div>"
            }
        },
        "description":"Returns the HTML for the object"
    },
    404:{
        "content":{
            "text/plain":{
               "example": "Product not available"
            }
        },
        "description":"A cleartext with error message"
    }

})



@router.get("/{id}", response_class=HTMLResponse)
def get_products_as_html(id:int):
    if id > len(products):
        out = "Product not found"
        return PlainTextResponse(content=out,media_type="text/plain")
    else:
        product_list = "".join(f"<li>{product}</li>" for product in products)
        html_content = f"""
        <html>
            <head>
                <title>Product List</title>
            </head>
            <body>
                <h1>Available Products</h1>
                <ul>
                    {product_list}
                </ul>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content,media_type="text/html")