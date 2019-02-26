from flask import Flask, request, json
from src.routes import router
import jwt


app = Flask(__name__)   
app.register_blueprint(router)

@app.route('/jwt/encode')
def jwtEncode():
    encode = jwt.encode({"nama":"nur imamhawari akbar"},"biocell",algorithm="HS256")    
    return encode

@app.route('/jwt/decode', methods=["POST"])
def jwtDecode():
    decode = jwt.decode(request.json["token"],"biocell",algorithms=["HS256"])    
    return str(decode)
