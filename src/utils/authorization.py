from flask import request, json, g
from .crypt import forEncrypt, forDecrypt
from .token import encode, decode
from functools import wraps
import jwt

def generateToken(data):
    data = forEncrypt(data)
    token = encode(data)

    return token

def verifyLogin(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):

        token = request.headers["Authorization"][7:]
        data = decode(token)
        username = forDecrypt(data["data"])
        
        g.username = username

        return f(*args, **kwargs)
    return decoratedFunction        