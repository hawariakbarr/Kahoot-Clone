from flask import Flask, request, json, abort, jsonify
from src.routes import router
import jwt

app = Flask(__name__)   
app.register_blueprint(router)

@app.route('/penjumlahan/<int:numb1>/<int:numb2>')
def penjumlahan(numb1, numb2):
    return jsonify({
        "hasil": numb1+numb2
    })
