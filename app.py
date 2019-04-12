from config import app
from db import db


db.init_app(app)

@app.before_first_request
def create_tables():
	db.create_all()  # will not recreate tables if they already exist