import flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or secrets.token_urlsafe(32)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
db.init_app(app)
