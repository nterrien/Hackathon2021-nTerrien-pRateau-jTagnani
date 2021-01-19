from bdd.database import db


class Reservation (db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    name = db.Column(db.Text)

