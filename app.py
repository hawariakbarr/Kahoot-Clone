from flask import Flask, request, json, abort
from src.routes import router
import jwt

app = Flask(__name__)   
app.register_blueprint(router)

@app.route('/tes')
def tes():
    abort(404)


