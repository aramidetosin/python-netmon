from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
import yaml

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
