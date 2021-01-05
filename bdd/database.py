from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_database():
    import bdd.models
    db.create_all()


def populate_database():
    from bdd.dbMethods import addTest

    cat1 = "test important"
    cat2 = "test pas important"
    test1 = "je fais une bdd"
    test2 = "je la teste"
    test3 = "j'essaie de la peupler"

    addTest (test1, cat1)
    addTest (test2, cat1)
    addTest (test3, cat2)


def clear_database():
    db.drop_all()