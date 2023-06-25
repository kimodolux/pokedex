import flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

db = SQLAlchemy()
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
db.init_app(app)
