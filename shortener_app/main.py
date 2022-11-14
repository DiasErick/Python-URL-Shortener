from fastapi import FastAPI, HTTPException
from . import schemas
import validators


app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to my first experience with API in Python!"

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise raise_bad_request("It seems that your provided URL it's not valid. Let's try again?")
    return f"TODO: Create database entry for: {url.target_url}"