from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_database():
    import bdd.models
    db.create_all()


def populate_database():
    return


def clear_database():
    db.drop_all()