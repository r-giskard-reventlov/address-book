from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'seldonplan'

CORS(app)

db = SQLAlchemy(app)

from seldon_address_book import api, models

db.create_all()
