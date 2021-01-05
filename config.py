import os
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///bdd/bdd.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
