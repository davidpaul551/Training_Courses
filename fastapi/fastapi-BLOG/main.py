from fastapi import FastAPI
from db import models
from db.database_creation import engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from routers import Post


app = FastAPI()

app.include_router(Post.router)

#database creation
models.Base.metadata.create_all(engine)

app.mount('/images',StaticFiles(directory='images'),name='images')


origins = [
    'http://localhost:3000'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)





