import secrets
import string
from sqlalchemy.orm import Session
from . import crud

def get_random_key(len: int = 5):
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(len))

def create_unique_key(db: Session, len: int = 5):    
    
    temp_key = get_random_key(len)
    while crud.get_db_url_key(db=db, key=temp_key):
        temp_key = get_random_key(len)

    return temp_key