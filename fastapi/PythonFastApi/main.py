from fastapi import FastAPI, HTTPException, WebSocket,status,Response,Request
from enum import Enum
from typing import Optional

from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
import time

from db.database import engine
from db import models
from exceptions import StoryException
from router import blog_get
from router import blog_post
from router import user
from router import article
from router import product
from auth import authentication
from router import file
from router import templates
from router import dependencies

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from client import html
app = FastAPI()

app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(dependencies.router)


@app.get('/hello')
def index():
    return {"message" : "hello World , Im Chitti"}

@app.post('/hello')
def index2():
    return {"message": "index 2 message"}

@app.exception_handler(StoryException)
def story_exception_handler(request:Request,exc:StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail':exc.name}
    )


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

# Endpoint
@app.websocket("/chat")
async def websocket_endpoint(websocket :WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)

# @app.exception_handler(HTTPException)
# def custom_handler(request:Request,exc:StoryException):
#     return PlainTextResponse(str(exc),status_code=400)

models.Base.metadata.create_all(engine)

origins=[
    'http://localhost:3000'
]

@app.middleware("http")
async def add_middlewares(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration']=str(duration)
    return response



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/files',StaticFiles(directory="files"),name='files')





