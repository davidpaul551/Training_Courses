from fastapi import FastAPI
from db import models
from db.database_creation import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from routers import user
from routers import post
from auth import authentication
from routers import comment


app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


models.Base.metadata.create_all(engine)


app.mount('/images',StaticFiles(directory='images'),name='images')