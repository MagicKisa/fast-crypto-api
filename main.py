from fastapi import FastAPI
from predictor import ScamPredictor
from pydantic import BaseModel
from cryptoApi import get_source_code
import requests

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis


class CodeItem(BaseModel):
    code: str


class FindItem(BaseModel):
    platform: str
    address: str


app = FastAPI()
model = ScamPredictor()


base_address = "0x9f589e3eabe42ebc94a44727b3f3531c0c877809"
base_platform = 'BNB'

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
async def root():
    """tell if app is up and running"""
    return {"message": "It's up"}


@app.post("/code_predict/")
# @cache(expire=30)
async def predict_by_code(item: CodeItem):
    """predict the class and probability of not scam crypto project
    by contract code of token"""
    return {"message": f"Legit is {model.predict(item.code)}"}


@app.get("/predict/")
@cache(expire=30)
async def predict_by_address_and_platform(address: str = base_address, platform: str = base_platform):
    """predict the class and probability of not scam crypto project
    by platform and contract address of token"""
    code = get_source_code(address, platform)
    return  {"message": f"Legit is {model.predict(code)}"}


@app.get("/code/")
@cache(expire=30)
async def get_code_by_address_and_platform(address: str = base_address, platform: str = base_platform):
    """requests the contract code by platform and contract address of token"""
    code = get_source_code(address, platform)
    return {"code": f"{code}"}


#@app.get("/model/")
#async def get_model():
#    """requests the contract code by platform and contract address of token"""
#    code = get_source_code(address, platform)
#    return {"code": f"{code}"}


@app.get("/secret/")
@cache(expire=5)
async def get_secret():
    """requests the contract code by platform and contract address of token"""
    url = "https://tools-api.robolatoriya.com/compliment"
    compliment = requests.get(url).json()['text']

    return {"very importrant message": f"{compliment}"}