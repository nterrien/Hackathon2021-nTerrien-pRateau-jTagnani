from bdd.database import db

class Test (db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text, db.ForeignKey('category.name'))

class Category (db.Model):
    __tablename__ = "category"
    name = db.Column(db.Text, primary_key=True)
    tests = db.relationship('Test', backref='test.id', lazy='dynamic')

class Visitor (db.Model):
    tablename = "visitor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)