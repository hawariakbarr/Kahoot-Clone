from flask import Flask
from src.routes import router

app = Flask(__name__)   
app.register_blueprint(router)