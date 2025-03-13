from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)


redis = get_redis_connection(
    host = 'redis-14376.c305.ap-south-1-1.ec2.redns.redis-cloud.com',
    port = 14376,
    password = 'OojWZRISmz9G9uEg6m3UDRMu7iBbE3AJ',
    decode_responses = True
)

class Product(HashModel):
    name:str
    price:float
    quantity:int
    class Meta:
        database=redis

@app.post('/product')
def create(product:Product):
    return product.save()