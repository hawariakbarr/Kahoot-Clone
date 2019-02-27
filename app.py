from flask import Flask, request, json
from src.routes import router
import jwt


app = Flask(__name__)   
app.register_blueprint(router)

