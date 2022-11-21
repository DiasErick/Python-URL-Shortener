from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:    
    key = keygen.create_unique_key(db = db)
    secret_key = key + "_" +  keygen.get_random_key(8)
    db_url = models.URL(target_url = url.target_url, secret_key = secret_key, key = key, is_active = True, clicks = 0)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)    
    return db_url

def get_db_url_key(db: Session, key: str) -> models.URL:
    db_url = db.query(models.URL).filter(models.URL.key == key, models.URL.is_active).first()
    return db_url

def get_db_url_secret(db: Session, secret: str)-> models.URL:
    db_url = db.query(models.URL).filter(models.URL.secret_key == secret, models.URL.is_active).first()
    return db_url

def update_db_url_click(db: Session, db_url: schemas.URL):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_secret(db: Session, secret_key: str)-> models.URL:
    db_url = get_db_url_secret(db = db,secret = secret_key )
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url