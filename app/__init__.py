from flask import Flask
from flask_login import LoginManager
from .config import Config

import mysql.connector

app = Flask(__name__)
app.config.from_object(Config)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # type: ignore


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passwordnt",
    database="notquiteourvle"
)

from app import views