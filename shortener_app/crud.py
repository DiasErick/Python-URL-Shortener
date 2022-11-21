from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    
    key = keygen.create_unique_key()
    secret_key = keygen.create_unique_key(8)

    db_url = models.URL(target_url = url.target_url, secret_key = secret_key, key = key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_key(db : Session, key: str):
    db_url = db.query(models.URL).filter(models.URL.key == key, models.URL.is_active)
    return db_url
