from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PurcahsedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
