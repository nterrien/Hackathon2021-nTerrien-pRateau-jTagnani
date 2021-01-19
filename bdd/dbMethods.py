from bdd.database import db
from bdd.models import Reservation



## Create
def addReservation (name, start, end):
    reservation = Reservation (name=name, start=start, end=end)
    db.session.add (reservation)
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas ajouter de réservation "
                "a cause de : %s" % e)
        db.session.rollback()



## Read
def findReservation (id):
    return Reservation.query.filter_by(id = id).first()



## Update
def updateReservation (id, name, start, end):
    reservation = findReservation (id)
    reservation.name = name
    reservation.start = start
    reservation.end = end
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas update une Reservation "
                "a cause de : %s" % e)
        db.session.rollback()



## Delete
def deleteReservation (id):
    Reservation.query.filter_by(id = id).delete()
    try :
        db.session.commit()
    except Exception as e:
        print("[1] Je ne peux pas supprimer une Reservation "
                "a cause de : %s" % e)
        db.session.rollback()
