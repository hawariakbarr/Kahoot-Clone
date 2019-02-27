import jwt
import os
from datetime import datetime, timedelta

def encode(data):
    payload = {
        "data": data,
        "exp": datetime.utcnow() + timedelta(days=10),
        "iat": datetime.utcnow()
    }
    encoded = jwt.encode(payload,os.getenv("SECRET"),algorithm="HS256").decode('utf-8')
    return encoded

def decode(data):
    decoded = jwt.decode(data,os.getenv("SECRET"),algorithms="HS256")    
    return decoded
