from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'seldonplan'

db = SQLAlchemy(app)

from seldon_address_book import views, models
