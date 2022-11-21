import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas, keygen, crud
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():    
    return "Welcome to my first experience with API in Python!"

@app.get("/all")
def reat_all():
    from shortener_app.database import SessionLocal
    from shortener_app.models import URL
    db = SessionLocal()
    return db.query(URL).all()
    
def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' does not exist"
    raise HTTPException(status_code = 404, detail=message)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
        
    db_url = crud.create_db_url(db, url.target_url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url

@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    if db_url := crud.get_db_url_key(db=db,key = models.URL.key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)