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
    __tablename__ = "visitor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    usages = db.relationship('NameUsage', backref='nameUsage.name', lazy='dynamic')

class NameUsage (db.Model):
    __tablename__ = "nameUsage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, db.ForeignKey('visitor.name'))
    usage = db.Column(db.Text)
    gender = db.Column(db.Text)
