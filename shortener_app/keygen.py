import secrets
import string

def get_random_key(len: int = 5):
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(len))